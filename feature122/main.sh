#!/bin/bash

awk '{print $7}' | awk 'NR % 2 == 1'
