#!/usr/bin/env python
# encoding: utf-8
# __author__ = 'Demon'

from seedemu.core import Emulator, Binding, Filter
from seedemu.compiler import Docker
from seedemu.services import EthereumService
from EthereumConsoleManager import EthereumConsoleManager

sim = Emulator()
eth = EthereumService()
esm = EthereumConsoleManager()

sim.load('base-component.bin')

# create eth node
e1 = eth.install("eth1")
e2 = eth.install("eth2")
e3 = eth.install("eth3")
e4 = eth.install("eth4")

# optionally, set boot nodes.
e1.setBootNode(True)
e2.setBootNode(True)

# optionally, set boot node http server port
e1.setBootNodeHttpPort(8081)

# add bindings
sim.addBinding(Binding('eth1', filter = Filter(asn = 150)))
sim.addBinding(Binding('eth2', filter = Filter(asn = 151)))
sim.addBinding(Binding('eth3', filter = Filter(asn = 152)))
sim.addBinding(Binding('eth4', filter = Filter(asn = 153)))

sim.addLayer(eth)
sim.render()

#Generate and deploy Smart Contract on node eth1
esm.startMinerInAllNodes(eth)
esm.deploySmartContractOn(e1, eth, "./examples/19-SmartContract/dummy.sol")
esm.createNewAccountInNode(e2, eth)

sim.compile(Docker(), './eth-private-network')