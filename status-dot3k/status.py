from kubernetes import client, config, utils
import dot3k.backlight as backlight
import dot3k.lcd as lcd
import dot3k.joystick as joystick
import time, json, math
from threading import Timer

#
#
#
def switchMode(new_mode):
  global mode, backlight_timer, deploy_index
  lcd.clear()
  
  if new_mode != mode:
    deploy_index = -1

  mode = new_mode
  
  # turn off backlight after 10 seconds
  if backlight_timer != None:
    backlight_timer.cancel()
  backlight_timer = Timer(4.0, backlight.off)
  backlight_timer.start() 

  if mode == joystick.UP:
    backlight.hue(0.4)
    lcd.write(f"Nodes:      /   ")
    lcd.write(f"Pods:       /   ")
    lcd.write(f"Deploy:     /   ")
    showKubeCounts()

  if mode == joystick.LEFT:
    backlight.hue(0.1)
    printNodes()
    showNodeMetrics()

  if mode == joystick.DOWN:
    deploy_index = deploy_index + 1
    if deploy_index >= deploy_max:
      deploy_index = 0    
    backlight.hue(0.7)
    showKubeDeploys()   

#
#
#
def showKubeCounts():
  nodes = v1.list_node(watch=False)
  nodes_ready = 0
  nodes_total = len(nodes.items)
  for node in nodes.items:
    for cond in node.status.conditions:
      if cond.type == "Ready" and cond.status == "True":
        nodes_ready = nodes_ready + 1

  lcd.set_cursor_position(9, 0)
  lcd.write(str(nodes_total).ljust(2))
  lcd.set_cursor_position(14, 0)
  lcd.write(str(nodes_ready).ljust(2))

  pods = v1.list_pod_for_all_namespaces(watch=False)
  pods_running = 0
  pods_total = len(pods.items)
  for pod in pods.items:
    if pod.status.phase == "Running": 
      pods_running = pods_running + 1

  lcd.set_cursor_position(9, 1)
  lcd.write(str(pods_total).ljust(2))
  lcd.set_cursor_position(14, 1)
  lcd.write(str(pods_running).ljust(2))  

  deploys = v1Apps.list_deployment_for_all_namespaces(watch=False)
  deploy_ready = 0
  deploy_total = len(deploys.items)
  for deploy in deploys.items:
    if deploy.status.ready_replicas == deploy.status.replicas: 
      deploy_ready = deploy_ready + 1

  lcd.set_cursor_position(9, 2)
  lcd.write(str(deploy_total).ljust(2))
  lcd.set_cursor_position(14, 2)
  lcd.write(str(deploy_ready).ljust(2))

#
#
#
def showNodeMetrics():
  # Get usage metrics from raw API call to /apis/metrics.k8s.io/v1beta1/nodes
  api_client = client.ApiClient()
  raw_resp = api_client.call_api('/apis/metrics.k8s.io/v1beta1/nodes/', 'GET', _preload_content=False)
  # Crazy conversion required 
  response_metrics = json.loads(raw_resp[0].data.decode('utf-8'))  

  # Call list Nodes
  nodes = v1.list_node()
  count = 0
  for node in nodes.items:
    if count > 2: break
    # Get name and cpu/mem capacity 
    name = node.metadata.name
    mem_capacity = utils.parse_quantity(node.status.allocatable["memory"])
    cpu_capacity = utils.parse_quantity(node.status.allocatable["cpu"])

    # Search node metrics we grabbed before keyed on node name
    node_metrics = next(n for n in response_metrics["items"] if n["metadata"]["name"] == name)
    mem_usage = utils.parse_quantity(node_metrics["usage"]["memory"])
    cpu_usage = utils.parse_quantity(node_metrics["usage"]["cpu"])

    cpu_perc = round((cpu_usage/cpu_capacity)*100)
    mem_perc = round((mem_usage/mem_capacity)*100) 

    lcd.set_cursor_position(7, count)
    lcd.write(f"{cpu_perc: 3}%")
    lcd.set_cursor_position(12, count)
    lcd.write(f"{mem_perc: 3}%")    
    count = count + 1

#
#
#
def printNodes():
  nodes = v1.list_node()
  count = 0
  for node in nodes.items:
    if count > 2: break
    name = node.metadata.name
    lcd.set_cursor_position(0, count)
    lcd.write(name+":")
    count = count + 1

#
#
#
def showKubeDeploys():
  global deploy_index, deploy_max
  #print(deploy_index)
  all_deploys = v1Apps.list_deployment_for_all_namespaces()

  deploy_max = 0
  deploys = []
  for deploy in all_deploys.items:
    if deploy.metadata.namespace != "kube-system": 
      deploys.append(deploy)

  deploy_max = len(deploys)
  lcd.set_cursor_position(0, 0)
  lcd.write(deploys[deploy_index].metadata.name[:16])
  lcd.set_cursor_position(0, 1)
  lcd.write(deploys[deploy_index].spec.template.spec.containers[0].image[:16])
  lcd.set_cursor_position(0, 2)
  lcd.write(f"replicas: {deploys[deploy_index].status.replicas}/{deploys[deploy_index].status.ready_replicas}")  

########################
# Entry point here
########################

config.load_kube_config()
v1 = client.CoreV1Api()
v1Apps = client.AppsV1Api()

backlight.off()
lcd.clear()
lcd.set_contrast(45)

# Switch modes with joystick
@joystick.on(joystick.UP)
def handle_u(pin):
  switchMode(pin)
@joystick.on(joystick.DOWN)
def handle_d(pin):
  switchMode(pin)
@joystick.on(joystick.LEFT)
def handle_l(pin):
  switchMode(pin)    
@joystick.on(joystick.RIGHT)
def handle_r(pin):
  switchMode(pin)

# Globals
deploy_index = 0
deploy_max = 0
backlight_timer = None
mode = joystick.UP

# Starting mode
switchMode(joystick.DOWN)

# Main loop
while True:
  if mode == joystick.UP:
    showKubeCounts()
  if mode == joystick.LEFT:
    showNodeMetrics()    
  if mode == joystick.DOWN:
    showKubeDeploys()      
  time.sleep(5)
