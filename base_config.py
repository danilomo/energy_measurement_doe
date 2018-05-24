server  = "foobar"

config = {
    "commands": {
        "ubuntu01": "./start_benchmark %s %s %s %s" % (cpu01, io01, net01, server ),
        "ubuntu02": "./start_benchmark %s %s %s %s" % (cpu02, io02, net02, server ),
    },    
    "experimentDuration": 60 * 4,
    "instances": {
        "ubuntu01": {
            "provider": "libvirt1"#,
            #"cpulimit": cpu01
        },
        "ubuntu02": {
            "provider": "libvirt1"#,
            #"cpulimit": cpu02
        }
    },
    "samplingInterval": 60,
    "measuringInterval": 50
}

provider_config = {
    "libvirt1": {
	"type": "libvirt",
	"parameters" : {
	    "url": "qemu:///system"
	},
	"instances" : {
	    "ubuntu01" : {
		"domain_name": "ubuntu02",
		"user_name": "teste",
		"password": "12345",
		"cpu_pin": {
		    "0": [1,0,0,0]
		}
	    },
	    "ubuntu02" : {
		"domain_name": "ubuntu02",
		"user_name": "teste",
		"password": "12345",
		"cpu_pin": {
		    "0": [1,0,0,0]
		}
	    }            
	}
    }
}

