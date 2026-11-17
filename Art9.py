class RequestorArtifactoryAPIView(APIView):
    def post(self, request):
        user, user_type, decoded = get_user(request)
        if isinstance(user, Response):
            return user
        from datetime import timezone
        from django.utils.dateparse import parse_datetime
        from django.utils import timezone as django_timezone

        sgp_id = request.data.get("sgpId")
        event_filter_status = request.data.get("eventFilterStatus")
        event_filter = (
            request.data.getlist("eventFilter")
            if hasattr(request.data, "getlist")
            else request.data.get("eventFilter", [])
        )

        if user_type in [
            Role.ROLE_TYPE_RQ,
        ]:
            return Response(
                {
                    "status": False,
                    "display_message": True,
                    "message": settings.ERRORS["unauth_access"],
                    "errors": settings.ERRORS["unauth_access"],
                    "data": [],
                },
                status=status.HTTP_422_UNPROCESSABLE_ENTITY,
            )

        if not sgp_id or not str(sgp_id).isdigit():
            return Response(
                {
                    "status": False,
                    "message": "There are incorrect values in the form",
                    "errors": {
                        "sgpId": ["The sgpId field is required and must be numeric."]
                    },
                    "display_message": False,
                    "data": [],
                },
                status=status.HTTP_422_UNPROCESSABLE_ENTITY,
            )

        if event_filter_status not in ["Yes", "No"]:
            return Response(
                {
                    "status": False,
                    "message": "There are incorrect values in the form",
                    "errors": {
                        "eventFilterStatus": [
                            "The eventFilterStatus must be Yes or No."
                        ]
                    },
                    "display_message": False,
                    "data": [],
                },
                status=status.HTTP_422_UNPROCESSABLE_ENTITY,
            )

        valid_events = [
            LogUpdate.STATUS_EVENT,
            LogUpdate.COMMENTS_EVENT,
            LogUpdate.DOC_EVENT,
            LogUpdate.EMAIL_EVENT,
            LogUpdate.INTAKE_EVENT,
            LogUpdate.DATE_EVENT,
            LogUpdate.RESP_EVENT,
            LogUpdate.ANALYZE_EVENT,
            LogUpdate.SEC_ANALYZE_EVENT,
            LogUpdate.ARTIFACT_EVENT,
            LogUpdate.AI_EVENT,
            LogUpdate.ATO_STATUS_EVENT,
            LogUpdate.RESET_INTAKE_EVENT,
            LogUpdate.RESET_REVIEW_EVENT,
            LogUpdate.CHANGE_SOLUTION_TYPE_EVENT,
            LogUpdate.RES_ASS_EVENT
        ]
        if event_filter_status == "Yes":
            if not event_filter:
                return Response(
                    {
                        "status": False,
                        "message": "There are incorrect values in the form",
                        "errors": {
                            "eventFilter": [
                                "The eventFilter field is required when eventFilterStatus is Yes."
                            ]
                        },
                        "display_message": False,
                        "data": [],
                    },
                    status=status.HTTP_422_UNPROCESSABLE_ENTITY,
                )

            for event in event_filter:
                try:
                    event_int = int(event)
                    if event_int not in valid_events:
                        return Response(
                            {
                                "status": False,
                                "message": "There are incorrect values in the form",
                                "errors": {
                                    "eventFilter": ["The selected filter is invalid"]
                                },
                                "display_message": False,
                                "data": [],
                            },
                            status=status.HTTP_422_UNPROCESSABLE_ENTITY,
                        )
                except (ValueError, TypeError):
                    return Response(
                        {
                            "status": False,
                            "message": "There are incorrect values in the form",
                            "errors": {
                                "eventFilter": ["The selected filter is invalid"]
                            },
                            "display_message": False,
                            "data": [],
                        },
                        status=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    )

        try:
            request_details = get_object_or_404(RequestorTeam, sgp_id=sgp_id)
        except RequestorTeam.DoesNotExist:
            return Response(
                {
                    "status": False,
                    "message": settings.ERRORS.get("invalid_request"),
                    "errors": settings.ERRORS.get("invalid_request"),
                    "display_message": True,
                    "data": [],
                },
                status=status.HTTP_422_UNPROCESSABLE_ENTITY,
            )

        access_error = check_user_access(
            user=user, request_instance=request_details, is_hold_data=True
        )

        if access_error:
            return Response(
                {
                    "status": False,
                    "message": access_error,
                    "errors": access_error,
                    "display_message": True,
                    "data": [],
                },
                status=status.HTTP_422_UNPROCESSABLE_ENTITY,
            )

        try:
            data = {}
            data["logEventList"] = LogUpdate.EVENT_TYPE_CHOICES

            if event_filter_status == "Yes" and event_filter:
                log_updates = (
                    LogUpdate.objects.filter(
                        request=request_details,
                        event__in=event_filter,
                    )
                    .filter(~Q(event=LogUpdate.SAR_LOG_EVENT))
                    .select_related("created_by")
                    .order_by("-created_date")
                )
            else:
                log_updates = (
                    LogUpdate.objects.filter(request=request_details)
                    .filter(~Q(event=LogUpdate.SAR_LOG_EVENT))
                    .select_related("created_by")
                    .order_by("-created_date")
                )

            serializer = LogUpdateSerializer(log_updates, many=True)
            log_update_data = list(serializer.data)

            artifact_qids = set()
            for item in log_update_data:
                if item.get("event") == LogUpdate.ARTIFACT_EVENT:
                    try:
                        artifact_qids.add(int(item["response_for"]))
                    except (ValueError, TypeError):
                        pass

            question_map = {}
            if artifact_qids:
                question_map = dict(
                    SpiPsiMaster.objects.filter(qid__in=artifact_qids).values_list(
                        "qid", "question_name"
                    )
                )

            for item in log_update_data:
                event = item.get("event")

                if event == LogUpdate.ARTIFACT_EVENT:
                    try:
                        item["response_for"] = question_map.get(
                            int(item["response_for"]), item["response_for"]
                        )
                    except (ValueError, TypeError):
                        pass

                elif event == LogUpdate.STATUS_EVENT:
                    if item.get("response_for") in [
                        LogUpdate.RES_FOR_REQUEST,
                        LogUpdate.RES_FOR_SUB_STATUS,
                    ]:
                        try:
                            item["old_value_str"] = RequestorTeam.STATUS_CHOICES.get(
                                int(item.get("old_value", "")),
                                item.get("old_value", "-"),
                            )
                        except (ValueError, TypeError):
                            item["old_value_str"] = item.get("old_value", "-")

                        try:
                            item["new_value_str"] = RequestorTeam.STATUS_CHOICES.get(
                                int(item.get("new_value", "")),
                                item.get("new_value", "-"),
                            )
                        except (ValueError, TypeError):
                            item["new_value_str"] = item.get("new_value", "-")

                elif event == LogUpdate.ATO_STATUS_EVENT:
                    try:
                        item["old_value_str"] = RequestorTeam.ATO_STATUS_CHOICES.get(
                            int(item.get("old_value", "")),
                            item.get("old_value", "-"),
                        )
                    except (ValueError, TypeError):
                        item["old_value_str"] = item.get("old_value", "-")

                    try:
                        item["new_value_str"] = RequestorTeam.ATO_STATUS_CHOICES.get(
                            int(item.get("new_value", "")),
                            item.get("new_value", "-"),
                        )
                    except (ValueError, TypeError):
                        item["new_value_str"] = item.get("new_value", "-")

                elif event == LogUpdate.INTAKE_EVENT:
                    item["response_for"] = (
                        f"Intake Form - {item.get('response_for', '')}"
                    )

                elif event in (LogUpdate.ANALYZE_EVENT, LogUpdate.SEC_ANALYZE_EVENT):
                    item["old_value_str"] = item.get("old_value", "-")
                    item["new_value_str"] = item.get("new_value", "")

                elif event == LogUpdate.RESET_INTAKE_EVENT or event == LogUpdate.RESET_REVIEW_EVENT or event == LogUpdate.CHANGE_SOLUTION_TYPE_EVENT or event == LogUpdate.RES_ASS_EVENT:
                    try:
                        item["old_value_str"] = RequestorTeam.STATUS_CHOICES.get(
                            int(item.get("old_value", "")),
                            item.get("old_value", "-"),
                        )
                    except (ValueError, TypeError):
                        item["old_value_str"] = item.get("old_value", "-")

                    try:
                        item["new_value_str"] = RequestorTeam.STATUS_CHOICES.get(
                            int(item.get("new_value", "")),
                            item.get("new_value", "-"),
                        )
                    except (ValueError, TypeError):
                        item["new_value_str"] = item.get("new_value", "-")

            include_doc_events = (
                event_filter_status == "Yes"
                and LogUpdate.DOC_EVENT in [int(e) for e in event_filter]
            ) or event_filter_status == "No"

            if include_doc_events:
                spi_psi_responses = (
                    SpiPsiResponse.objects.filter(request=request_details)
                    .exclude(filename="")
                    .exclude(filename__isnull=True)
                    .select_related("question")
                )

                requestor_storage = settings.GLOBAL_CONFIG.get(
                    "requestor_storage", "requestor"
                )

                for response in spi_psi_responses:
                    if not response.filename:
                        continue

                    old_value = "-"

                    if response.question_id == 43:
                        response_for = (
                            f"Vendor/Third Party 1 - {response.question.question_name}"
                        )
                    else:
                        response_for = response.question.question_name

                    location = f"||storage/{requestor_storage}/{sgp_id}/"
                    new_value = location + response.filename.replace("||", location)

                    doc_created_date = (
                        getattr(response, "created_date", None)
                        or request_details.created_on
                    )
                    doc_created_date_str = (
                        django_timezone.localtime(doc_created_date).strftime(
                            "%Y-%m-%d %H:%M:%S"
                        )
                        if doc_created_date
                        else None
                    )

                    log_update_data.append(
                        {
                            "event": LogUpdate.DOC_EVENT,
                            "old_value": old_value,
                            "new_value": new_value,
                            "response_for": response_for,
                            "created_date": doc_created_date_str,
                            "event_string": LogUpdate.get_event_type_display(
                                LogUpdate.DOC_EVENT
                            ),
                            "created_by_name": (
                                request_details.request_owner.get_full_name()
                                if request_details.request_owner
                                else "Unknown"
                            ),
                            "old_value_str": old_value,
                            "new_value_str": new_value,
                        }
                    )

                third_party_responses = (
                    ThirdPartyResponse.objects.filter(request=request_details)
                    .exclude(filename="")
                    .exclude(filename__isnull=True)
                    .select_related("question")
                    .order_by("sequence")
                )

                for idx, response in enumerate(third_party_responses):
                    if not response.filename:
                        continue

                    old_value = "-"
                    response_for = f"Vendor/Third Party {idx + 2} - {response.question.question_name}"

                    location = f"||storage/{requestor_storage}/{sgp_id}/"
                    new_value = location + response.filename.replace("\\", location)

                    doc_created_date = (
                        getattr(response, "created_date", None)
                        or request_details.created_on
                    )
                    doc_created_date_str = (
                        django_timezone.localtime(doc_created_date).strftime(
                            "%Y-%m-%d %H:%M:%S"
                        )
                        if doc_created_date
                        else None
                    )

                    log_update_data.append(
                        {
                            "event": LogUpdate.DOC_EVENT,
                            "old_value": old_value,
                            "new_value": new_value,
                            "response_for": response_for,
                            "created_date": doc_created_date_str,
                            "event_string": LogUpdate.get_event_type_display(
                                LogUpdate.DOC_EVENT
                            ),
                            "created_by_name": (
                                request_details.request_owner.get_full_name()
                                if request_details.request_owner
                                else "Unknown"
                            ),
                            "old_value_str": old_value,
                            "new_value_str": new_value,
                        }
                    )

            def get_sort_key(item):
                created_date = item.get("created_date")
                if not created_date:
                    return django_timezone.make_aware(datetime.min, timezone.utc)

                if isinstance(created_date, datetime):
                    dt = created_date
                else:
                    created_date_str = str(created_date).strip()
                    dt = parse_datetime(created_date_str)
                    if dt is None:
                        try:
                            dt = datetime.strptime(
                                created_date_str, "%Y-%m-%d %H:%M:%S"
                            )
                        except ValueError:
                            return django_timezone.make_aware(
                                datetime.min, timezone.utc
                            )

                if django_timezone.is_naive(dt):
                    dt = django_timezone.make_aware(dt, timezone.utc)

                return dt

            log_update_data.sort(key=get_sort_key, reverse=True)

            data["logUpdateData"] = log_update_data
            data["page_title"] = f"View Logs - {sgp_id}"
            data["projectName"] = request_details.project_name
            data["solutionName"] = request_details.solution_name
            data["solutionType"] = request_details.solution_type
            data["solutionType"] = RequestorTeam.SOLUTION_TYPE_CHOICES.get(
                request_details.solution_type
            )
            data["sgpId"] = sgp_id
            data["total"] = len(log_update_data)

            return Response(
                {
                    "status": True,
                    "display_message": False,
                    "message": "Log list fetched",
                    "errors": [],
                    "data": data,
                },
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            return Response(
                {
                    "status": False,
                    "message": settings.ERRORS.get("syntax_error_access"),
                    "errors": [str(e)],
                    "display_message": True,
                    "data": [],
                },
                status=status.HTTP_422_UNPROCESSABLE_ENTITY,
            )
