#!/bin/bash
awk 'NR % 2 == 0 {print $7}'
