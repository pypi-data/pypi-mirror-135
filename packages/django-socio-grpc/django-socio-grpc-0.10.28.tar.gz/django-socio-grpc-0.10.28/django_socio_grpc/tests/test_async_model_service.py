import os

from asgiref.sync import async_to_sync
from django.test import TestCase

from django_socio_grpc import generics, mixins
from fakeapp.grpc import fakeapp_pb2
from fakeapp.grpc.fakeapp_pb2_grpc import (
    UnitTestModelControllerStub,
    add_UnitTestModelControllerServicer_to_server,
)
from fakeapp.models import UnitTestModel
from fakeapp.serializers import UnitTestModelSerializer

from .grpc_test_utils.fake_grpc import FakeGRPC


class UnitTestService(generics.AsyncModelService, mixins.AsyncStreamModelMixin):
    queryset = UnitTestModel.objects.all()
    serializer_class = UnitTestModelSerializer


class TestAsyncModelService(TestCase):
    def setUp(self):
        os.environ["GRPC_ASYNC"] = "True"
        self.fake_grpc = FakeGRPC(
            add_UnitTestModelControllerServicer_to_server, UnitTestService.as_servicer()
        )

        self.create_instances()

    def tearDown(self):
        os.environ["GRPC_ASYNC"] = ""
        self.fake_grpc.close()

    def create_instances(self):
        for idx in range(10):
            title = "z" * (idx + 1)
            text = chr(idx + ord("a")) + chr(idx + ord("b")) + chr(idx + ord("c"))
            UnitTestModel(title=title, text=text).save()

    def test_async_create(self):
        grpc_stub = self.fake_grpc.get_fake_stub(UnitTestModelControllerStub)
        request = fakeapp_pb2.UnitTestModel(title="fake", text="text")
        response = grpc_stub.Create(request=request)

        self.assertNotEqual(response.id, None)
        self.assertEqual(response.title, "fake")
        self.assertEqual(response.text, "text")
        self.assertEqual(UnitTestModel.objects.count(), 11)

    def test_async_list(self):
        grpc_stub = self.fake_grpc.get_fake_stub(UnitTestModelControllerStub)
        request = fakeapp_pb2.UnitTestModelListRequest()
        response = grpc_stub.List(request=request)

        self.assertEqual(len(response.results), 10)

    def test_async_retrieve(self):
        unit_id = UnitTestModel.objects.first().id
        grpc_stub = self.fake_grpc.get_fake_stub(UnitTestModelControllerStub)
        request = fakeapp_pb2.UnitTestModelRetrieveRequest(id=unit_id)
        response = grpc_stub.Retrieve(request=request)

        self.assertEqual(response.title, "z")
        self.assertEqual(response.text, "abc")

    def test_async_update(self):
        unit_id = UnitTestModel.objects.first().id
        grpc_stub = self.fake_grpc.get_fake_stub(UnitTestModelControllerStub)
        request = fakeapp_pb2.UnitTestModel(id=unit_id, title="newTitle", text="newText")
        response = grpc_stub.Update(request=request)

        self.assertEqual(response.title, "newTitle")
        self.assertEqual(response.text, "newText")

    def test_async_destroy(self):
        unit_id = UnitTestModel.objects.first().id
        grpc_stub = self.fake_grpc.get_fake_stub(UnitTestModelControllerStub)
        request = fakeapp_pb2.UnitTestModelDestroyRequest(id=unit_id)
        grpc_stub.Destroy(request=request)

        self.assertFalse(UnitTestModel.objects.filter(id=unit_id).exists())

    def test_async_stream(self):
        grpc_stub = self.fake_grpc.get_fake_stub(UnitTestModelControllerStub)
        request = fakeapp_pb2.UnitTestModelStreamRequest()
        grpc_stub.Stream(request=request)

        responses = async_to_sync(self.fake_grpc.grpc_channel.context.read)()
        response_list = [response for response in responses]

        self.assertEqual(len(response_list), 10)
