import asyncio
from unittest import mock

from loafer.dispatcher import LoaferDispatcher
from loafer.exceptions import ProviderError
from loafer.managers import LoaferManager
from loafer.runners import LoaferRunner


def test_dispatcher():
    manager = LoaferManager(routes=[])
    assert manager.dispatcher
    assert isinstance(manager.dispatcher, LoaferDispatcher)


def test_default_runner():
    manager = LoaferManager(routes=[])
    assert manager.runner
    assert isinstance(manager.runner, LoaferRunner)


def test_custom_runner():
    runner = mock.Mock()
    manager = LoaferManager(routes=[], runner=runner)
    assert manager.runner
    assert isinstance(manager.runner, mock.Mock)


def test_on_future_errors():
    manager = LoaferManager(routes=[])
    manager.runner = mock.Mock()
    future = asyncio.Future()
    future.set_exception(ProviderError)
    manager.on_future__errors(future)

    assert manager.runner.stop.called
    assert manager.runner.stop.called_once_with()


def test_on_loop__stop():
    manager = LoaferManager(routes=[])
    manager.dispatcher = mock.Mock()
    manager._future = mock.Mock()
    manager.on_loop__stop()

    assert manager.dispatcher.stop_providers.called
    assert manager._future.cancel.called