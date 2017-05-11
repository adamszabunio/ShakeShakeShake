#!/usr/bin/env python3
"""classifies magnitudes into three levels"""
def mag_category(x):
      if x <= 2.5:
          return("0-2.5, not felt")
      elif x > 2.5 and x < 5.5:
          return("2.5-5.5, felt, minor damage")
      else:
          return("5.5 and above, potential for major damage")
