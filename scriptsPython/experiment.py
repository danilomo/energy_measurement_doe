from git import Repo
import json
import os


class Experiment:
	def __init__(self):
		pass

	def getConfig(self):
		raise NotImplementedError()

	def getProviderConfig(self):
		raise NotImplementedError()

class CPUExperiment(Experiment):

	def __init__(self, limit):
		self._limit = limit
		self._duration = 60

	def getExperimentConfig(self):
		conf = {
			"provider": "libvirt1",
			"experimentDuration": self._duration,
			"samplingInterval": 5,
			"instances": ["ubuntu01", "ubuntu02"],
			"commands": {
				"ubuntu01": "./stressCPU.sh " + str(self._limit) + " " + str(self._duration),
				"ubuntu02": ":"
			}
		}

		return conf

	def getProviderConfig(self):
		conf = {
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
								"0": [1, 0, 0, 0]
							}
						},
						"ubuntu02" : {
							"domain_name": "ubuntu02",
							"user_name": "teste",
							"password": "12345",
							"cpu_pin": {
								"0": [1, 0, 0, 0]
							}
						}
					}
				}
			}

		return conf

	def __str__(self):
		return "cpu_experiment_" + str(self._limit)


def makeExperimentsDirectories( l ):

	for e in l:
		folder = str(e)
		os.mkdir(folder)

		Repo.clone_from("https://github.com/danilomo/energy_measurement_scripts.git",folder)


                # To copy a folder instead cloning from the repository

                #os.mkdir(folder)
                #os.system( "cp -a ../template/. " + folder )


		filename = folder + "/configFiles/config.json"
		configFile = json.dumps(e.getExperimentConfig(), sort_keys=True, indent = 4 ) + "\n"
		os.remove(filename)

		with open(filename, 'w+') as f:
			f.write(configFile)

		filename = folder + "/configFiles/provider_config.json"
		providerConfig = json.dumps(e.getProviderConfig(), sort_keys=True, indent = 4 ) + "\n"
		os.remove(filename)

		with open(filename, 'w+') as f:
			f.write(providerConfig)


l = []
for i in range(5, 20, 5):
	e = CPUExperiment( i )
	e._duration = 60
	l.append( e )

makeExperimentsDirectories( l )
