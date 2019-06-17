from functions import *

server1  = "f23"
server2  = "f33"

time = 60 * 5

config = {
    "commands": {
        "ubuntu01": "./start_benchmark.sh %s %s %s %s %s" % (time, cpu01, io01, net01, server1 ),
    },    
    "experimentDuration": time,
    "instances": {
        "ubuntu01": {
            "provider": "libvirt1"
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
	    }           
	}
    }
}

