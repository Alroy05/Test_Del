# Fix for the ADO event filter on the artifactory (activity logs) page
# =====================================================================
#
# File to change : the view in Art9.py -> RequestorArtifactoryAPIView.post
# Lines          : the `valid_events = [...]` list (Art9.py lines 62-79)
#
# Why it fails
# ------------
# The filter dropdown is filled from LogUpdate.EVENT_TYPE_CHOICES (sent as
# "logEventList"), which has 18 event types. The view then checks the selected
# values against a separate hand-written `valid_events` list that only has 16.
# The two missing ones are:
#
#     LogUpdate.FINDINGS_EVENT = 14   ("Findings")
#     LogUpdate.ADO_EVENT      = 15   ("ADO")
#
# So choosing "ADO" (or "Findings") sends eventFilter=15 (or 14), the check
# `if event_int not in valid_events` is true, and the view returns
# 422 "The selected filter is invalid" instead of the filtered logs.
#
# Nothing else needs to change: the query (`event__in=event_filter`), the
# serializer and the frontend already handle these two event types.
#
#
# The change
# ----------
# REMOVE this block:
#
#         valid_events = [
#             LogUpdate.STATUS_EVENT,
#             LogUpdate.COMMENTS_EVENT,
#             LogUpdate.DOC_EVENT,
#             LogUpdate.EMAIL_EVENT,
#             LogUpdate.INTAKE_EVENT,
#             LogUpdate.DATE_EVENT,
#             LogUpdate.RESP_EVENT,
#             LogUpdate.ANALYZE_EVENT,
#             LogUpdate.SEC_ANALYZE_EVENT,
#             LogUpdate.ARTIFACT_EVENT,
#             LogUpdate.AI_EVENT,
#             LogUpdate.ATO_STATUS_EVENT,
#             LogUpdate.RESET_INTAKE_EVENT,
#             LogUpdate.RESET_REVIEW_EVENT,
#             LogUpdate.CHANGE_SOLUTION_TYPE_EVENT,
#             LogUpdate.RES_ASS_EVENT
#         ]
#
# and PUT THIS in its place (indent it 8 spaces, like the list it replaces):

# Every event type offered in the filter dropdown is a valid filter.
# EVENT_TYPE_CHOICES is the same dict returned as "logEventList", so the
# dropdown and this check can no longer drift apart. SAR_LOG_EVENT (13)
# is not in EVENT_TYPE_CHOICES, so it stays rejected as before.
valid_events = list(LogUpdate.EVENT_TYPE_CHOICES.keys())

#
# Alternative (smallest possible edit)
# ------------------------------------
# If you would rather keep the hand-written list, add these two lines to it:
#
#             LogUpdate.FINDINGS_EVENT,
#             LogUpdate.ADO_EVENT,
#
# The downside is that the next event type added to EVENT_TYPE_CHOICES will
# hit the same bug unless this list is updated too.
#
#
# How to check it
# ---------------
# POST /request/requestor-artifactory/ with form data
#     sgpId=<a request id>, eventFilterStatus=Yes, eventFilter=15
# Before: 422, errors.eventFilter = ["The selected filter is invalid"]
# After : 200, logUpdateData contains only rows with event == 15
#         (an empty list if that request has no ADO logs)
