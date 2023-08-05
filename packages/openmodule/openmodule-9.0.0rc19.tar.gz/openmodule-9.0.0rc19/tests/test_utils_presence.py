from datetime import datetime
from functools import partial

import orjson
from typing import Optional

import time
from unittest import TestCase

from openmodule.core import init_openmodule, shutdown_openmodule
from openmodule.models.base import Direction, Gateway
from openmodule.models.presence import PresenceBaseMessage, PresenceRPCRequest, PresenceRPCResponse, PresenceBaseData, \
    PresenceMedia
from openmodule.models.vehicle import MakeModel, LPRMedium, LPRCountry, PresenceAllIds
from openmodule.rpc import RPCServer
from openmodule.utils.presence import PresenceListener
from openmodule_test.eventlistener import MockEvent
from openmodule_test.presence import PresenceSimulator
from openmodule_test.zeromq import ZMQTestMixin


class BasePresenceTest(ZMQTestMixin, TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.core = init_openmodule(self.zmq_config(), context=self.zmq_context())
        self.presence_sim = PresenceSimulator("gate_in", Direction.IN, lambda x: self.zmq_client.send(b"presence", x))

        self.presence = PresenceListener(self.core.messages)
        self.on_enter = MockEvent()
        self.on_forward = MockEvent()
        self.on_backward = MockEvent()
        self.on_change = MockEvent()
        self.on_leave = MockEvent()
        self.presence.on_enter.append(self.on_enter)
        self.presence.on_forward.append(self.on_forward)
        self.presence.on_backward.append(self.on_backward)
        self.presence.on_change.append(self.on_change)
        self.presence.on_leave.append(self.on_leave)
        self.wait_for_dispatcher(self.core.messages)

    def tearDown(self):
        shutdown_openmodule()
        super().tearDown()


class PresenceTest(BasePresenceTest):
    def test_cannot_use_present_vehicle_without_gate(self):
        with self.assertRaises(AssertionError) as e:
            self.presence.present_vehicle.json()
        self.assertIn("please access the present vehicle per gate", str(e.exception))

        self.presence.gate = "test"
        val = self.presence.present_vehicle
        self.assertIsNone(val)

    def test_double_entry(self):
        self.presence_sim.enter(self.presence_sim.vehicle().lpr("A", "G ARIVO1"))
        self.on_enter.wait_for_call()
        self.assertEqual("G ARIVO1", self.presence.present_vehicles["gate_in"].lpr.id)

        MockEvent.reset_all_mocks()
        self.presence_sim.current_present = None
        with self.assertLogs() as cm:
            self.presence_sim.enter(self.presence_sim.vehicle().lpr("A", "G ARIVO2"))
            self.on_enter.wait_for_call()
            self.on_leave.wait_for_call()
        self.assertEqual("G ARIVO2", self.presence.present_vehicles["gate_in"].lpr.id)
        self.assertIn("A leave will be faked", str(cm))

    def test_faulty_exit(self):
        with self.assertLogs() as cm:
            self.presence_sim.current_present = self.presence_sim.vehicle().lpr("A", "G ARIVO1")
            self.presence_sim.leave()
            time.sleep(1)
            self.assertEqual({}, self.presence.present_vehicles)
        self.assertIn("The leave will be ignored", str(cm))

        self.presence_sim.enter(self.presence_sim.vehicle().lpr("A", "G ARIVO1"))
        self.on_enter.wait_for_call()
        self.assertEqual("G ARIVO1", self.presence.present_vehicles["gate_in"].lpr.id)

        self.presence_sim.current_present = self.presence_sim.vehicle().lpr("A", "G ARIVO2")
        with self.assertLogs() as cm:
            self.presence_sim.leave()
            self.on_leave.wait_for_call()
            self.assertEqual({}, self.presence.present_vehicles)
        self.assertIn("We are fake-leaving the currently present vehicle", str(cm))

    def test_vehicle_id_change(self):
        vehicle_0 = self.presence_sim.vehicle()
        self.presence_sim.enter(vehicle_0)
        self.on_enter.wait_for_call()
        self.assertEqual(vehicle_0.vehicle_id, self.presence.present_vehicles["gate_in"].id)

        vehicle_1 = self.presence_sim.vehicle().lpr("A", "G ARIVO1")
        self.presence_sim.change_vehicle_and_id(vehicle_1)
        self.on_change.wait_for_call()

        self.assertEqual(vehicle_1.vehicle_id, self.presence.present_vehicles["gate_in"].id)

        self.presence_sim.leave()
        self.on_leave.wait_for_call()

        self.assertIsNone(self.presence.present_vehicles.get("gate_in"))

    def test_lpr_change(self):
        vehicle_0 = self.presence_sim.vehicle().lpr("A", "GARIVO1")
        self.presence_sim.enter(vehicle_0)
        self.on_enter.wait_for_call()
        self.assertEqual("GARIVO1", self.presence.present_vehicles["gate_in"].lpr.id)

        vehicle_0.lpr("A", "GARIVO2")
        self.presence_sim.change(vehicle_0)
        self.on_change.wait_for_call()
        self.assertEqual("GARIVO2", self.presence.present_vehicles["gate_in"].lpr.id)

    def test_make_model_change(self):
        vehicle_0 = self.presence_sim.vehicle().lpr("A", "GARIVO1")
        self.presence_sim.enter(vehicle_0)
        self.on_enter.wait_for_call()
        self.assertEqual("GARIVO1", self.presence.present_vehicles["gate_in"].lpr.id)

        vehicle_0.set_make_model(MakeModel(make="TESLA", make_confidence=0.7, model="UNKNOWN", model_confidence=-1.0))
        self.presence_sim.change(vehicle_0)
        self.on_change.wait_for_call()
        self.assertEqual("TESLA", self.presence.present_vehicles["gate_in"].make_model.make)

    def test_normal(self):
        self.presence_sim.enter(self.presence_sim.vehicle().lpr("A", "G ARIVO1"))
        self.on_enter.wait_for_call()
        self.assertEqual("G ARIVO1", self.presence.present_vehicles["gate_in"].lpr.id)

        self.presence_sim.leave()
        self.on_leave.wait_for_call()
        self.assertEqual({}, self.presence.present_vehicles)

    def test_other_calls(self):
        vehicle = self.presence_sim.vehicle().lpr("A", "G ARIVO1")

        self.presence_sim.forward(vehicle)
        self.on_forward.wait_for_call()

        self.presence_sim.backward(vehicle)
        self.on_backward.wait_for_call()

        self.presence_sim.enter(vehicle)
        self.on_enter.wait_for_call()

        vehicle_changed = vehicle.nfc("asdf")
        self.presence_sim.change(vehicle_changed)
        self.on_change.wait_for_call()
        self.on_change.reset_mock()


class PresenceTestUtilsTest(BasePresenceTest):
    def test_vehicle_id_change_is_enforced(self):
        vehicle = self.presence_sim.vehicle().lpr("A", "G ARIVO1")
        self.presence_sim.enter(vehicle)

        with self.assertRaises(AssertionError) as e:
            self.presence_sim.change_vehicle_and_id(vehicle)
        self.assertIn("vehicle id must change", str(e.exception))

        self.presence_sim.change_vehicle_and_id(self.presence_sim.vehicle().lpr("A", "G ARIVO1"))
        self.on_change.wait_for_call()


class GateFilterTest(BasePresenceTest):
    def setUp(self) -> None:
        super().setUp()
        self.presence2 = PresenceListener(self.core.messages, "gate_in")
        self.on_enter2 = MockEvent()
        self.presence2.on_enter.append(self.on_enter2)

    def tearDown(self):
        super().tearDown()

    def test_gate_filter(self):
        self.presence_sim.enter(self.presence_sim.vehicle().lpr("A", "G ARIVO1"))

        self.on_enter.wait_for_call()
        self.assertIn("gate_in", self.presence.present_vehicles.keys())
        self.presence.present_vehicles = {}
        self.on_enter2.wait_for_call()
        self.assertIn("gate_in", self.presence2.present_vehicles.keys())
        self.presence2.present_vehicles = {}

        MockEvent.reset_all_mocks()

        sim_out = PresenceSimulator("gate_out", Direction.OUT, lambda x: self.zmq_client.send(b"presence", x))
        sim_out.enter(sim_out.vehicle().lpr("A", "G ARIVO2"))
        self.on_enter.wait_for_call()

        self.assertIn("gate_out", self.presence.present_vehicles.keys())
        with self.assertRaises(TimeoutError):
            self.on_enter2.wait_for_call()

        self.assertEqual({}, self.presence2.present_vehicles)


class PresenceSimulatorTest(TestCase):
    message: Optional[PresenceBaseMessage] = None

    def setUp(self) -> None:
        super().setUp()
        self.message = None

    def test_presence_alias_fields_serialization(self):
        sim = PresenceSimulator("gate1", Direction.IN, partial(setattr, self, "message"))
        sim.enter(sim.vehicle().qr("test"))
        sim.forward()
        message = orjson.loads(self.message.json_bytes())
        self.assertIn("leave-time", message)


class PresenceRPCTest(ZMQTestMixin, TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.core = init_openmodule(self.zmq_config(), context=self.zmq_context())
        self.wait_for_dispatcher(self.core.messages)
        self.presence_sim = PresenceSimulator("gate_in", Direction.IN, lambda x: self.zmq_client.send(b"presence", x))
        self.rpc_server = RPCServer(context=self.core.context)
        self.rpc_server.register_handler("tracking", "get-present", PresenceRPCRequest, PresenceRPCResponse,
                                         self.on_reply)
        self.rpc_server.run_as_thread()
        self.present = False

    def tearDown(self):
        self.rpc_server.shutdown()
        shutdown_openmodule()
        super().tearDown()

    def on_reply(self, request: PresenceRPCRequest, _) -> PresenceRPCResponse:
        """
        Emulates Trackings Presence RPC
        """
        if self.present:
            return PresenceRPCResponse(presents=[
                PresenceBaseData(vehicle_id=1, source="gate_in", present_area_name="gate_in",
                                 last_update=datetime.utcnow(), gateway=Gateway(gate="gate_in", direction="in"),
                                 medium=PresenceMedia(lpr=LPRMedium(id="T EST 1")), all_ids=PresenceAllIds())])
        else:
            return PresenceRPCResponse(presents=[])

    def test_presence_rpc_plate(self):
        self.present = True
        self.presence = PresenceListener(self.core.messages, gate="gate_in")
        self.presence.init_present_vehicles()
        self.assertNotEqual({}, self.presence.present_vehicles)

    def test_presence_rpc_no_plate(self):
        self.present = False
        self.presence = PresenceListener(self.core.messages, gate="gate_in")
        self.presence.init_present_vehicles()
        self.assertEqual({}, self.presence.present_vehicles)

    def test_presence_rpc_only_allowed_for_gates(self):
        self.presence = PresenceListener(self.core.messages)
        with self.assertRaises(AssertionError) as e:
            self.presence.init_present_vehicles()
        self.assertIn("if the gate is set", str(e.exception))
