from functions import *

server1  = "f23"
server2  = "f33"

time = 60 * 1

config = {
    "commands": {
        "ubuntu01": "./start_benchmark.sh %s %s %s %s %s" % (time, cpu1(cpu01), io1(io01), net1(net01), server1 ),
        "ubuntu02": "./start_benchmark.sh %s %s %s %s %s" % (time, cpu1(cpu02), io1(io02), net1(net02), server2 ),
    },    
    "experimentDuration": time,
    "instances": {
        "ubuntu01": {
            "provider": "libvirt1",
            "cpushare": cpu2(cpu01),
            "iolimit" :  io2(io01)
        },
        "ubuntu02": {
            "provider": "libvirt1",
            "cpushare": cpu2(cpu02),
            "iolimit" :  io2(io02)
        }
    },
    "samplingInterval": 20,
    "measuringInterval": 15
}

provider_config = {
    "libvirt1": {
	"type": "libvirt",
	"parameters" : {
	    "url": "qemu:///system"
	},
	"instances" : {
	    "ubuntu01" : {
		"domain_name": "ubuntu01",
		"user_name": "teste",
		"password": "12345",
		"cpu_pin": {
		    "0": [1,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0]
		}
	    },
	    "ubuntu02" : {
		"domain_name": "ubuntu02",
		"user_name": "teste",
		"password": "12345",
		"cpu_pin": {
		    "0": [1,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0]
		}
	    }            
	}
    }
}

