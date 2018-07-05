server  = "f33"

time = 60 * 5

config = {
    "commands": {
        "ubuntu01": "./start_benchmark.sh %s %s %s %s %s" % (time, cpu01, io01, net01, server ),
        "ubuntu02": "./start_benchmark.sh %s %s %s %s %s" % (time, cpu02, io02, net02, server ),
    },    
    "experimentDuration": time,
    "instances": {
        "ubuntu01": {
            "provider": "libvirt1",
            "cpushare": 20
        },
        "ubuntu02": {
            "provider": "libvirt1",
            "cpushare": 80
        }
    },
    "samplingInterval": 60,
    "measuringInterval": 55
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

