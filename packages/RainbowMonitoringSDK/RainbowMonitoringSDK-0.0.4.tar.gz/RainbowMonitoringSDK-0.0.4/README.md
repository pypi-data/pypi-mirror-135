<h1><strong>Rainbow Monitoring Agent</strong></h1>
<hr>
<br>
<h1>Overview</h1>
The **Rainbow Monitoring Agent** provides a containerized service that captures monitoring metrics from the underlying fog node infrastructure, the containerized execution environments and/or performance metrics from the deployed IoT applications.
In the initial implementation, NetData is used as the main *metric collector* and on top of that are built the sensing and disseminating functionalities of Rainbow's project.

<br>
<h1>Features</h1>

- Coordinates the metric collection process
- Easy to reuse for various layers of the fog continuum with different metric collectors
- Takes into consideration rapid changes that occur due to the enforcement of runtime scaling actions

<br>
<h1>Components</h1>

* **Probes:** The actual metric collectors that adhere to a common metric collection interface
* **Exporters:** Exports the formatted or aggregated data to different endpoints
* **Controller:** Orchistrates the execution of Sensing Units (Probes) and Dissemination Units (Exporters)

<br>
<h1>Architecture</h1>

The architecture of the RAINBOW Monitoring follows an agent-based architecture that embraces the producer-consumer paradigm. This approach provides interoperable, scalable and real-time monitoring for extracting both infrastructure and application behaviour data from deployed IoT services. 
The RAINBOW Monitoring runs in a non-intrusive and transparent manner to underlying fog environments as neither the metric collection process nor the metric distribution and storage are dependent to underlying platform APIs (e.g., fog-node specific) and communication mechanisms. The following image depicts a high-level and abstract overview of the Monitoring Agent.

<br>

<p align="center">
  <img alt="Moniroting Architecture" src="https://www.cs.ucy.ac.cy/~jgeorg02/assets/img/monitoring-architecture.jpg" />
</p>

<br>
<h1>Configurations</h1>

The Monitoring Agent consists of general interfaces for both probes and exporters. This can facilitate the process of adding new custom sensing and dissemination units that the user may want to use. In addition, users can configure their sensing and dissemination units through a YAML file, where they can specify the metric groups that they are mostly interested in collecting metrics for. At the first version of the monitoring agent the default monitoring unit used is Netdata.

In the following yaml example we can see that we have 3 main hierarchies:

* **node_id:** is the unique identifier of the node
* **sensing-units:** are the probes that will collect metrics from the node
* **dissemination-units:** represents the exporters that will disseminate metrics


Regarding **sensing-units**, a user can define the **general-periodicity**, which is the general sensing rate of the probe. A user can define multiple sensing-units and they can specify the **periodicity** for each one of them. They can also specify which metric groups they don't want the probe to collect metrics for with the **disabled-metric-groups** option, and with the **metric-groups** they can override sensing preferences on specific groups.

In the **dissemination-units** section it's possible to configurate basic information for each of the exporters the user wants to use, for example the **port**, **hostname**, **periodicity**, etc.


``` yaml

    node_id: raspberry_pi_4_in_region_3
    
    # configuration for probes
    sensing-units:
        # general sensing rate
        general-periodicity: 5s
        # specific implementation of the sensing interface
        DefaultMonitoring:
            periodicity: 5s
            # metric groups that the system will not start at all 
            # (e.g. CPU, memory, disk, network)
            disabled-metric-groups:
                - "disk"
            #override sensing preferences on specific groups
            metric-groups:
                - name: "memory"
                  periodicity: 15s
                - name: "cpu"
                  periodicity: 1s
        # specific implementation of sensing interface for user-defined metrics
        UserDefinedMetrics:
            periodicity: 5s
            sources:
            	- "/rainbow-metrics/"
    
    # configuration for exporters
    dissemination-units:
         RestAPI:
             port: 4200
             path: /api/metrics
         RAINBOWStorage:
             hostname: ignite-server
             port: 50000
             delivery: push
             periodicity: 30s
             aggregation: no
```
<br>
<h1>How to add a new Probe</h1>

Developers are free to create their own Monitoring Probes and Metrics, by adhering to the properties defined in the Monitoring Probe API which provides a common API interface and abstractions hiding the complexity of the underlying Probe functionality. The following figure depicts the implementation of an ExampleProbe which includes the definition of two SimpleMetric’s, denoted as metric1 and metric2, which periodically report random values respectively. In turn, a CounterMetric and a TimerMetric are also defined. In this figure it is observed that for a user to develop a Monitoring Probe, he/she must only provide default values for the Probe periodicity and a name, a short description of the offered functionality, and a concrete implementation of the collect() method which, as denoted by the name, defines how metric values are updated.
  
```python

    from probes.Metric import SimpleMetric, CounterMetric, DiffMetric, TimerMetric
    from probes.Probe import Probe
    
    
    class ExampleProbe(Probe):
    
        def __init__(self, name="ExampleProbe", periodicity=5):
	    super(ExampleProbe, self).__init__(name, periodicity)

	    self.myMetric1 = SimpleMetric('myMetric1', '%', 
            'random double between 0 and 10', 0, 10)

	    self.myMetric2 = SimpleMetric('myMetric2', '#', 
            'random int between 0 and 1000', 0, 1000, higherIsBetter=False)

    	self.myMetric3 = CounterMetric('myMetric3', '#', 
            'counter incrementing by 1 and resetting at 20', maxVal=20)

	    self.myMetric4 = DiffMetric('myMetric4', '#', 
            'scaled difference from previous val')

	    self.myMetric5 = TimerMetric('myMetric5', maxVal=10)
    
	    self.add_metric(self.myMetric1)
	    self.add_metric(self.myMetric2)
	    self.add_metric(self.myMetric3)
	    self.add_metric(self.myMetric4)
	    self.add_metric(self.myMetric5)

        def get_desc(self):
	    return "ExampleProbe collects some dummy metrics..."

        def collect(self):
	    self.myMetric5.timer_reset_and_start()

	    d = random.uniform(0, 100)
	    i = random.randint(0, 1000)

	    self.myMetric1.set_val(d)
	    self.myMetric2.set_val(i)
	    self.myMetric3.inc()
	    self.myMetric4.update(i)
	
	    time.sleep(d)
	    self.myMetric5.timer_end()
  ```

Probes' metrics may take other advanced forms, denoted as metric handlers. The user is also able to define the metric handlers they prefer for their custom probe.

<br>

<h2 align="center"> Metric Handlers</h2>
<hr>

| SimpleMetric | CounterMetric | TimerMetric | DiffMetric |
| ------------ | ------------- | ----------- | ---------- |
| Emits a single value for a referenced metric where the value is given by an external process. Is considered the base upon which all other metric handlers are extended from. | Emits a counter-increased value for a reference metric based on either a pre-defined increment (e.g., +1) or a given increment. | Emits the time consumed for the completion of a referenced task (e.g., API call). | Emits the proportional difference of the current collected value from the previous value. |

<br>

<h1>Install</h1>

The whole monitoring agent runs in the container and the user needs only to run the docker build command.

	docker build -t rainbow-monitoring:v0.01 .

The default configurations of the service are already injected and are placed at ``config.yaml`` file.
Users can override the configurations by injecting a new config file to the ``/code/configs.yaml`` folder of the container.

<br>

<h1>How to Store Custom Metrics:</h1>

```python
from RainbowMonitoringSDK.utils.annotations import RainbowUtils

#  example of rabbit mq channel rate
RainbowUtils.store(float(rabbitmq_channel_created_rate), 
                    'rabbitmq_channel_created_rate', 
                    'Cps', 
                    'created channel rate from rabbitmq')
  ```

<br>

<h1>Representative Monitoring Metrics</h1>
The following table lists some of the many metrics that the Rainbow Monitoring framework collects:

| Type of Metrics | Metric Group | Metric |
| --------------- | ------------ | ------ |
| System-level | CPU | **Cpu Utilization** |
| System-level | CPU | **Cpu Utilization per Core** |
| System-level | CPU | **Total Number of Interrupts per CPU** |
| System-level | Memory | **Total Available Memory** |
| System-level | Memory | **Committed Memory**, is the sum of all memory which has been allocated by processes |
| System-level | Memory | **Kernel Memory**, is the total amount of memory being used by the kernel |
| System-level | Disks | **Disk I/O Bandwidth**, for each disk |
| System-level | Disks | **Disk Busy Time**, measures the amount of time the disk was busy with something |
| System-level | Disks | **Disk Space Usage**, the amount of disk space that is available, -used or reserved- |
| System-level | Network | **IPv4/IPv6 Sockets**, the number of IPv4 or IPv6 sockets used at the current time |
| System-level | Network | **IPv4/IPv6 Packets**, the number of IPv4 or IPv6 packets received/transmitted from/to the node |
| System-level | Network | **IPv4/IPv6 TCP/UTP Packets**, the number of IPv4 or IPv6 TCP/UTP packets received/transmitted from/to the node |
| System-level | Network | **IPv4/IPv6 TCP/UTP Connections**, the amount of TCP/UTP open connections |
| System-level | Network Interfaces | **Network Interface Utilization**, amount of traffic that the interface has received and sent |
| System-level | Network Interfaces | **Network Interface Packet Traffic**, number of packets that the interface has received and sent |
| Container-level | CPU | **CPU Utilization** |
| Container-level | CPU | **CPU Utilization Per Core** |
| Container-level | Memory | **Memory in/out rate (MiB/s)** |
| Container-level | Memory | **Memory usage (in GB)** |
| Container-level | Memory | **Memory utilization (%)** |
| Container-level | Network Interfaces | **Network Interface Utilization**, amount of traffic that the interface has received and sent |
| Container-level | Network Interfaces | **Network Interface Packet Traffic**, number of packets that the interface has received and sent |

