#!/usr/bin/env python3
# This will be very barebones, at least for now

ESC = '\033'

COLORS= {
      'BLACK':   0,
      'RED':     1, 
      'GREEN':   2,
      'YELLOW':  3,
      'BLUE':    4,
      'PURPLE':  5,
      'CYAN':    6,
      'WHITE':   7
      }

def FG( color, bold = False ):
   if bold:
      BOLD="1;"
   else:
      BOLD = ""
   return f'{ESC}[3{COLORS[color]}m'

def BG( color, bold = False ):
   if bold:
      BOLD="1;"
   else:
      BOLD = ""
   return f'{ESC}[4{COLORS[color]}m'

def reset():
   return f'{BG("BLACK")}{FG("WHITE")}'



