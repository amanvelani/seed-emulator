#!/usr/bin/env python3
# encoding: utf-8

from seedemu import *
from examples.internet.B03_hybrid_internet import hybrid_internet
from examples.blockchain.D00_ethereum_poa import component_poa

def run(dumpfile = None, hosts_per_as=3, total_eth_nodes=20, total_accounts_per_node=2):

    # Run and load the pre-built Internet component
    emuA = Emulator()
    hybrid_internet.run(dumpfile='./component_base.bin', hosts_per_as=hosts_per_as)
    emuA.load('./component_base.bin')

    # Run and load the pre-built Ethereum component
    emuB = Emulator()
    component_poa.run(dumpfile='./component_poa.bin', 
                      total_eth_nodes=total_eth_nodes, 
                      total_accounts_per_node=total_accounts_per_node)
    emuB.load('./component_poa.bin')

    # Merge the two pre-built components
    emu = emuA.merge(emuB, DEFAULT_MERGERS)

    # Check if the size of total_eth_nodes is larger than the size of the total hosts
    base: Base = emu.getLayer('Base')
    asns = []
    for asn in base.getAsns():
        if len(base.getAutonomousSystem(asn).getHosts()) > 0:
            asns.append(asn)
    assert hosts_per_as * len(asns) >= total_eth_nodes, f'the total hosts size({hosts_per_as*len(asns)}) is smaller than the total_eth_nodes({total_eth_nodes}).'

    eth:EthereumService = emu.getLayer('EthereumService')
    blockchain: Blockchain =  eth.getBlockchainByName(eth.getBlockchainNames()[0])

    asnCounter = 0
    # Get all the server names and bind them to physical nodes
    for _, servers in blockchain.getAllServerNames().items():
        for server in servers:
           emu.addBinding(Binding(server, filter = Filter(asn = asns[asnCounter%len(asns)], nodeName=f'host_{asnCounter//len(asns)}')))
           asnCounter += 1

    # Generate output
    if dumpfile is not None:
        emu.dump(dumpfile)
    else:
        emu.render()
        docker = Docker(etherViewEnabled=True)
        emu.compile(docker, './output', override=True)

if __name__ == "__main__":
    run()
