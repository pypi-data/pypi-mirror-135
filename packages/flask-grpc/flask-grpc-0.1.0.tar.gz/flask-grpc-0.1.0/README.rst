flask-grpc
====================

A grpc client for Flask.

Usage
-------

init

.. code-block:: python

    channel_wrapper = ChannelWrapper(
        target="gaea-partner-python-grpc-dev-cuwmnyhgmq-uc.a.run.app:443",
        secure=True,
        credentials=grpc.ssl_channel_credentials(),
    )
    channel_wrapper.init_app(app)

    health_stub = StubWrapper(health_pb2_grpc.HealthStub, channel_wrapper)

views

.. code-block:: python

    @app.route("/grpc")
    def grpc_api():
        reply = health_stub.Check(health_pb2.HealthCheckRequest())
        return f"grpc response: {reply}"
