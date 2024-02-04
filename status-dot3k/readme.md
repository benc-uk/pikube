# Kubernetes Status Display LCD - Display-o-tron 3000

Sample code for displaying the status of your cluster in various ways on a external LCD board attached to one of the Raspberry Pis

You'll need a [Display-o-tron 3000](https://shop.pimoroni.com/products/display-o-tron-hat)

Pre Install

```bash
curl https://get.pimoroni.com/displayotron | bash
```

This command will fail at the end with an error like "error: externally-managed-environment", but don't worry, we resolve that below!

Copy the `status-dot3k` folder from this repo to the master node

```bash
scp -r ./status-dot3k master:~
```

SSH into the master node and run the following

```bash
cd ~/status-dot3k
python -m venv .venv
source .venv/bin/activate
pip install -r ./requirements.txt
chmod +x ./status.py
```

Run the script (make sure your venv is still activated!)

```bash
./status.py
```
