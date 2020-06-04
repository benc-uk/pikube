from kubernetes import client, config, watch
import unicornhat as unicorn
import math

# Set up colours for various pod phases
COLOURS = {
  "Running": (0, 255, 0),
  "Pending": (252, 169, 3),
  "Failed": (200, 0, 0),
  "Succeeded": (28, 204, 235)
}

# Load Kubernetes config file $HOME/.kube/config
config.load_kube_config()

# Global state, a dictionary of pods and statuses
pods = dict()

# Connect to Kubenetes API
v1 = client.CoreV1Api()
w = watch.Watch()

# Unicorn LED panel
unicorn.set_layout(unicorn.HAT)
unicorn.rotation(0)
unicorn.brightness(0.4)
width,height=unicorn.get_shape()

# Update all LEDs with current pod status 
def updateLEDs():
  i = 0
  unicorn.off()
  for pod_key in pods.keys():
    c = COLOURS[ pods[pod_key] ]
    unicorn.set_pixel(math.floor(i / width), i % width, c[0], c[1], c[2])
    i = i + 1
  unicorn.show()

# Subscribe to Kubernetes API event stream
for event in w.stream(v1.list_pod_for_all_namespaces):
  obj = event['object']
  evt_type = event['type']
  # Create a unique key namespace + pod name  
  key = f"{obj.metadata.namespace}_{obj.metadata.name}"
  phase = obj.status.phase

  # Various event types modify pod state store
  if evt_type == "ADDED":
    pods[key] = phase
  if evt_type == "MODIFIED":
    pods[key] = phase
  if evt_type == "DELETED":
    del pods[key]

  # Update the display
  updateLEDs()
