#!/usr/bin/env python3
# encoding: utf-8

from seedemu import *
from lib.services.EthereumService.EthUtil import CustomGenesis
from lib.services.EthereumService.EthereumService import CustomBlockchain
import web3
import sys

emu = Makers.makeEmulatorBaseWith10StubASAndHosts(1)

if len(sys.argv) == 1:
    platform = "amd"
else:
    platform = sys.argv[1]

platform_mapping = {"amd": Platform.AMD64, "arm": Platform.ARM64}
docker = Docker(etherViewEnabled=True, platform=platform_mapping[platform], internetMapPort=8081)

# Create the Ethereum layer
eth = EthereumService(override=True)

blockchain = eth.createBlockchain(chainName="POA", consensus=ConsensusMechanism.POA)
blockchain.__class__ = CustomBlockchain

initBal = 10**8
blockchain.addLocalAccount(address='0xF5406927254d2dA7F7c28A61191e3Ff1f2400fe9',
                            balance=30)
blockchain.addLocalAccount(address='0x2e2e3a61daC1A2056d9304F79C168cD16aAa88e9', 
                            balance=9999999)
blockchain.addLocalAccount(address='0x4e59b44847b379578588920cA78FbF26c0B4956C', balance=0)

# with open('./test/test1/Hello.bin-runtime', 'r') as f:
#     runtime_bytecode = web3.toBytes(hexstr=f.read().strip())

with open('./test/test3/MyERC20Token.bin-runtime', 'r') as f:
    runtime_bytecode = web3.Web3.toHex(hexstr=f.read().strip())

# Add the read bytecode to the blockchain under the specified address
blockchain.addCode('0x4e59b44847b379578588920cA78FbF26c0B4956C', runtime_bytecode)

# Create blockchain nodes (POA Ethereum)
e5 = blockchain.createNode("poa-eth5")
e6 = blockchain.createNode("poa-eth6")
e7 = blockchain.createNode("poa-eth7")
e8 = blockchain.createNode("poa-eth8")

# Set bootnodes on e5. The other nodes can use these bootnodes to find peers.
# Start mining on e5,e6
e5.setBootNode(True).unlockAccounts().startMiner()
e6.unlockAccounts().startMiner()

# Enable ws and http connections
# Set geth ws port to 8541 (Default : 8546)
e5.enableGethWs().setGethWsPort(8541)
e5.enableGethHttp()
e6.enableGethHttp()
e7.enableGethHttp()

# Customizing the display names (for visualization purpose)
emu.getVirtualNode("poa-eth5").setDisplayName("Ethereum-POA-5")
emu.getVirtualNode("poa-eth6").setDisplayName("Ethereum-POA-6")
emu.getVirtualNode("poa-eth7").setDisplayName("Ethereum-POA-7")
emu.getVirtualNode("poa-eth8").setDisplayName("Ethereum-POA-8")

# Binding virtual nodes to physical nodes
emu.addBinding(Binding("poa-eth5", filter=Filter(asn=160, nodeName="host_0")))
emu.addBinding(Binding("poa-eth6", filter=Filter(asn=161, nodeName="host_0")))
emu.addBinding(Binding("poa-eth7", filter=Filter(asn=162, nodeName="host_0")))
emu.addBinding(Binding("poa-eth8", filter=Filter(asn=163, nodeName="host_0")))

# Add the ethereum layer
emu.addLayer(eth)

emu.render()

# If output directory exists and override is set to false, we call exit(1)
# updateOutputdirectory will not be called
emu.compile(docker, "./output", override=True)
