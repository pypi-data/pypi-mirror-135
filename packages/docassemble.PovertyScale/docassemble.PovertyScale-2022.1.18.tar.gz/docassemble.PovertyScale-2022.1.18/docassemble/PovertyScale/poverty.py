# pre-load
import json
import sys
from docassemble.webapp.app_object import app
from docassemble.base.util import path_and_mimetype, log
from typing import Union
from flask import jsonify, request, Response

__all__ = ['poverty_scale_income_qualifies',
           'get_poverty_scale_data',
           'poverty_scale_get_income_limit'
          ]

ps_poverty_scale_json_path = path_and_mimetype(f"{__package__}:data/sources/federal_poverty_scale.json")[0]

@app.route("/poverty_guidelines", methods=['GET'])
def get_poverty_guidelines():
  results = get_poverty_scale_data()
  if results:
    return jsonify(results)
  else:
    return Response("{'error': 'Unable to load poverty guidelines from disk.'}", status=503, mimetype="application/json")

@app.route("/poverty_guidelines/household_size/<household_size>", methods=['GET'])
def get_household_poverty_guideline(household_size):
  if (request.args) and str(request.args.get('state')).lower() in ['ak','hi']:
    state = str(request.args.get('state')).lower()
  else:
    state = None
  if (request.args) and request.args.get('multiplier'):
    multiplier = int(request.args.get('multiplier'))
  else:
    multiplier = 1
  results = poverty_scale_get_income_limit(int(household_size), multiplier=multiplier, state=state)
  ps_data = get_poverty_scale_data()
  if isinstance(ps_data, dict):
    update_year = ps_data.get('poverty_level_update_year')
  else:
    update_year = -1
  if results:
    return jsonify({'amount': results, 'update_year': update_year})
  else:
    return Response("{'error': 'Unable to retrieve poverty guidelines.'}", status=503, mimetype="application/json")

@app.route("/poverty_guidelines/qualifies/household_size/<household_size>", methods=['GET'])
def get_household_qualifies(household_size):
  if not request.args or not request.args.get('income'):
    return Response("{'error': 'Income is required'}", 400, mimetype="application/json")
  try:
    income = int(request.args.get('income'))
  except ValueError:
    return Response("{'error': 'Invalid income value. Please provide an integer.'}", 400, mimetype="application/json")
  if str(request.args.get('state')).lower() in ['ak','hi']:
    state = str(request.args.get('state')).lower()
  else:
    state = None
  if request.args.get('multiplier'):
    multiplier = int(request.args.get('multiplier'))
  else:
    multiplier = 1
  results = poverty_scale_income_qualifies(income, int(household_size), multiplier=multiplier, state=state)
  ps_data = get_poverty_scale_data()
  if isinstance(ps_data, dict):
    update_year = ps_data.get('poverty_level_update_year')
  else:
    update_year = -1
  if not results is None:
    return jsonify({'qualifies': results, 'update_year': update_year})
  else:
    return Response("{'error': 'Unable to retrieve poverty guidelines.'}", status=503, mimetype="application/json")  
  
def get_poverty_scale_data():
  ps_data = {}
  try:
    with open(ps_poverty_scale_json_path) as f:
      ps_data = json.load(f)
  except FileNotFoundError:
    log(f"Cannot determine poverty scale: unable to locate file {ps_poverty_scale_json_path}")
  except json.JSONDecodeError as e:
    log(f"Cannot determine poverty scale: is {ps_poverty_scale_json_path} a valid JSON file? Error was {e}")
  
  return ps_data

def poverty_scale_get_income_limit(household_size:int=1, multiplier:int=1, state=None)->Union[int, None]:
  """
  Return the income limit matching the given household size.
  """
  ps_data = get_poverty_scale_data()
  if not ps_data:
    return None
  if state and state.lower() == 'hi':
    poverty_base = int(ps_data.get("poverty_base_hi"))
    poverty_increment = int(ps_data.get("poverty_increment_hi"))
  elif state and state.lower() == 'ak':
    poverty_base = int(ps_data.get("poverty_base_ak"))
    poverty_increment = int(ps_data.get("poverty_increment_ak"))
  else:
    poverty_base = int(ps_data.get("poverty_base"))
    poverty_increment = int(ps_data.get("poverty_increment"))
  additional_income_allowed = household_size * poverty_increment
  household_income_limit = (poverty_base + additional_income_allowed) * multiplier
  
  return household_income_limit

def poverty_scale_income_qualifies(total_monthly_income:float, household_size:int=1, multiplier:int=1, state=None)->Union[bool,None]:
  """
  Given monthly income, household size, and an optional multiplier, return whether an individual
  is at or below the federal poverty level.
  
  Returns None if the poverty level data JSON could not be loaded.
  """
  # Globals: poverty_increment and poverty_base
  household_income_limit = poverty_scale_get_income_limit(household_size=household_size, multiplier=multiplier, state=state)
  
  if not household_income_limit:
    return None
  
  return int((household_income_limit)/12) >=  int(total_monthly_income)
