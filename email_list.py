"""
"""

import phantom.rules as phantom
import json
from datetime import datetime, timedelta, time

def on_start(container):
    phantom.debug('on_start() called')
    
    # call 'decision_2' block
    decision_2(container=container)

    return

def add_list_1(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None):
    phantom.debug('add_list_1() called')
    
    filtered_artifacts_data_1 = phantom.collect2(container=container, datapath=['filtered-data:filter_1:condition_1:artifact:*.cef.toEmail'])
    
    phantom.debug("filtered_data: {}".format(filtered_artifacts_data_1))
    
    now = int("{:%s}".format(datetime.now()))

    filtered_artifacts_item_1_0 = [item[0] for item in filtered_artifacts_data_1]
    
    phantom.debug("filtered_artifact: {}".format(filtered_artifacts_item_1_0))
    timestamped_list = [[item[0],now] for item in filtered_artifacts_item_1_0]
    phantom.debug("timestamp_list: {}".format(timestamped_list))

    phantom.add_list("email_supression_24hr", timestamped_list)

    return

# check if email exists in our list. I.e. we've sent an email already to the 'toEmail'
def decision_2(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None):
    phantom.debug('decision_2() called')

    # check for 'if' condition 1
    matched_artifacts_1, matched_results_1 = phantom.condition(
        container=container,
        conditions=[
            ["artifact:*.cef.toEmail", "not in", "custom_list:email_supression_24hr"],
        ])

    # if email not in list add to custom_list
    if matched_artifacts_1 or matched_results_1:
        add_list_1(action=action, success=success, container=container, results=results, handle=handle)
        return

    # else check if the email is expired to update it
    decision_3(action=action, success=success, container=container, results=results, handle=handle)

    return

def decision_3(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None):
    phantom.debug('decision_3() called')
    
    # in 'long' format timestamp
    day_ago = int("{:%s}".format(datetime.now())) - 86400

    # is the email in list for more than 1 day
    matched_artifacts_1, matched_results_1 = phantom.condition(
        container=container,
        conditions=[
            ["custom_list:email_supression_24hr[artifact:*.cef.toEmail]", "<=", day_ago],
        ])

    # then update_list
    if matched_artifacts_1 or matched_results_1:
        update_list(action=action, success=success, container=container, results=results, handle=handle)
        return

    return

#placeholder for new Phantom release.
def update_list(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None):
    phantom.debug('update_list() called')
    
    template = """{0}"""

    # parameter list for template variable replacement
    parameters = [
        "",
    ]

    phantom.format(container=container, template=template, parameters=parameters, name="update_list")

    return

def on_finish(container, summary):
    phantom.debug('on_finish() called')
    # This function is called after all actions are completed.
    # summary of all the action and/or all detals of actions 
    # can be collected here.

    # summary_json = phantom.get_summary()
    # if 'result' in summary_json:
        # for action_result in summary_json['result']:
            # if 'action_run_id' in action_result:
                # action_results = phantom.get_action_results(action_run_id=action_result['action_run_id'], result_data=False, flatten=False)
                # phantom.debug(action_results)

    return