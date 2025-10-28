#!/bin/bash

awk '{print $7}' | awk 'NR % 1 == 0'
