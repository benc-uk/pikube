from kubernetes import client, config, utils
import unicornhat as unicorn
import json, math, time

# Load Kubernetes config file $HOME/.kube/config
config.load_kube_config()

# Connect to Kubenetes API
v1 = client.CoreV1Api()

unicorn.set_layout(unicorn.HAT)
unicorn.rotation(0)
unicorn.brightness(0.4)
width,height=unicorn.get_shape()

def drawBarRed(bar_width, row):
  for x in range(0, bar_width):
    unicorn.set_pixel(x, row, 255, math.floor((x/width)*255), 0)

def drawBarGreen(bar_width, row):
  for x in range(0, bar_width):
    unicorn.set_pixel(x, row, math.floor((x/width)*255), 160, 0)

while True:
  # Get usage metrics from raw API call to /apis/metrics.k8s.io/v1beta1/nodes
  api_client = client.ApiClient()
  raw_resp = api_client.call_api('/apis/metrics.k8s.io/v1beta1/nodes/', 'GET', _preload_content=False)
  # Crazy conversion required 
  response_metrics = json.loads(raw_resp[0].data.decode('utf-8'))  
  
  # Call list Nodes
  nodes = v1.list_node()

  node_index = 0
  unicorn.off()
  for node in nodes.items:
    # Get name and cpu/mem capacity 
    name = node.metadata.name
    mem_capacity = utils.parse_quantity(node.status.allocatable["memory"])
    cpu_capacity = utils.parse_quantity(node.status.allocatable["cpu"])

    # Search node metrics we grabbed before keyed on node name
    node_metrics = next(n for n in response_metrics["items"] if n["metadata"]["name"] == name)
    mem_usage = utils.parse_quantity(node_metrics["usage"]["memory"])
    cpu_usage = utils.parse_quantity(node_metrics["usage"]["cpu"])

    cpu_led_max = round((cpu_usage/cpu_capacity)*width)
    mem_led_max = round((mem_usage/mem_capacity)*width) 
    drawBarRed(cpu_led_max, node_index)
    drawBarGreen(mem_led_max, node_index+1)
    # Skip three lines, so leaves a gap 
    # NOTE! Only works with three nodes!!
    node_index = node_index + 3
  unicorn.show()
  time.sleep(5)
