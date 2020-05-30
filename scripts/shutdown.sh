#!/bin/bash

ssh pi@master sudo shutdown now
ssh pi@node-1 sudo shutdown now
ssh pi@node-2 sudo shutdown now
