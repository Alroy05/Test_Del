class GenerateCombineSarTemplateAPIView(APIView):
    def post(self, request) -> Response:
        user, user_type, _ = get_user(request)
        if isinstance(user, Response):
            return user

        serializer = GenerateCombinedSarTemplateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {
                    "status": False,
                    "message": "There are incorrect values in the form",
                    "errors": serializer.errors,
                    "display_message": False,
                    "data": [],
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        validated_data = serializer.validated_data
        sgp_id = validated_data["sgpId"]
        sar_template_data = validated_data.get("sarTemplateData")
        overall_risk = validated_data.get("overallRisk", "")
        submit_id = validated_data["submitId"]
        sar_comments = validated_data.get("sarComments", "")
        ato_status = validated_data.get("atoStatus", None)

        try:
            request_obj = RequestorTeam.objects.filter(sgp_id=sgp_id).first()
            if request_obj is None:
                return Response(
                    {
                        "status": False,
                        "message": settings.ERRORS["invalid_request"],
                        "errors": settings.ERRORS["invalid_request"],
                        "display_message": True,
                        "data": [],
                    },
                    status=status.HTTP_422_UNPROCESSABLE_ENTITY,
                )

            is_post_cutoff = is_request_created_after_cutoff(request_obj)

            checkUserAccess = check_user_access(user, request_obj)
            if checkUserAccess:
                return Response(
                    {
                        "status": False,
                        "message": checkUserAccess,
                        "errors": checkUserAccess,
                        "display_message": True,
                        "data": [],
                    },
                    status=status.HTTP_401_UNAUTHORIZED,
                )

            if "secRiskAcceptDoc" in request.FILES:
                file_check = check_file_type(request.FILES["secRiskAcceptDoc"])
                if file_check:
                    return Response(
                        {
                            "status": False,
                            "message": file_check,
                            "errors": file_check,
                            "display_message": False,
                            "data": [],
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                    )

            with transaction.atomic():
                if overall_risk:
                    LogUpdate.objects.create(
                        request=request_obj,
                        event=LogUpdate.RESP_EVENT,
                        old_value=request_obj.overall_risk or "-",
                        new_value=overall_risk,
                        response_for="SAR overall risk",
                        created_by=user,
                        user_role=user.current_role,
                    )
                    request_obj.overall_risk = overall_risk.replace(" ", "")
                    request_obj.save()

                if isinstance(sar_template_data, str):
                    parsed = json.loads(sar_template_data.strip())
                    sar_data_dict = parsed[0] if isinstance(parsed, list) else parsed
                elif isinstance(sar_template_data, list):
                    sar_data_dict = sar_template_data[0]
                else:
                    sar_data_dict = sar_template_data

                header_data = {
                    "input_sar_data": sar_data_dict,
                    "sar_comments": html.escape(sar_comments) if sar_comments else "",
                    "submit_id": submit_id,
                    "sgp_id": request_obj.sgp_id,
                    "created_by": user.id,
                }

                set_comb_sar_template_data(header_data)

                if sar_comments:
                    LogUpdate.objects.create(
                        request=request_obj,
                        event=LogUpdate.COMMENTS_EVENT,
                        old_value="-",
                        new_value=sar_comments,
                        response_for=LogUpdate.RES_FOR_CLEARANCE_COMMENT,
                        created_by=user,
                        user_role=user.current_role,
                    )

                if "secRiskAcceptDoc" in request.FILES:
                    location = (
                        f"{settings.RESULT_STORAGE}"
                        f"{settings.RISK_ACCEPT_STORAGE}/{sgp_id}"
                    )
                    file_name = store_media("secRiskAcceptDoc", request, location)
                    full_location = f"{settings.STORAGE_PATH}{location}/"
                    file_name_arr = file_name.split(";")
                    file_log = full_location + f"||{full_location}".join(file_name_arr)

                    LogUpdate.objects.create(
                        request=request_obj,
                        event=LogUpdate.DOC_EVENT,
                        old_value="-",
                        new_value=file_log,
                        response_for=LogUpdate.RES_FOR_CLEARANCE_COMMENT,
                        created_by=user,
                        user_role=user.current_role,
                    )

                old_status = request_obj.sub_status
                new_status = old_status
                email_extra = None
                action_allowed = False
                current_user_nm = f"{user.first_name} {user.last_name}"
                msg = "Update Access Not Allowed"

                if submit_id == "sar_ipg_reject":
                    if user_type in [
                        Role.ROLE_TYPE_AU,
                        Role.ROLE_TYPE_SECURITY_OFFICER,
                    ]:
                        if is_post_cutoff:
                            new_status = RequestorTeam.STATUS_COMB_IPG_TEMPLATE_REVIEW
                            request_obj.status = new_status
                            old_sub_status = request_obj.sub_status
                            request_obj.sub_status = (
                                RequestorTeam.SUB_STATUS_SECURITY_REVIEW
                            )
                            if ato_status:
                                new_ato_status = int(ato_status)
                                old_ato_status = request_obj.ato_status
                                if str(new_ato_status) != str(old_ato_status):
                                    LogUpdate.objects.create(
                                        request=request_obj,
                                        event=LogUpdate.ATO_STATUS_EVENT,
                                        old_value=str(old_ato_status),
                                        new_value=str(new_ato_status),
                                        response_for="ATO Status",
                                        created_by=user,
                                        user_role=user.current_role,
                                    )
                                request_obj.ato_status = ato_status
                            request_obj.save()

                            LogUpdate.objects.create(
                                request=request_obj,
                                event=LogUpdate.STATUS_EVENT,
                                old_value=str(old_status),
                                new_value=str(new_status),
                                response_for=LogUpdate.RES_FOR_REQUEST,
                                created_by=user,
                                user_role=user.current_role,
                            )
                            LogUpdate.objects.create(
                                request=request_obj,
                                event=LogUpdate.STATUS_EVENT,
                                old_value=str(old_sub_status),
                                new_value=str(request_obj.sub_status),
                                response_for=LogUpdate.RES_FOR_SUB_STATUS,
                                created_by=user,
                                user_role=user.current_role,
                            )
                            LogUpdate.objects.create(
                                request=request_obj,
                                event=LogUpdate.SAR_LOG_EVENT,
                                old_value="-",
                                new_value=header_data.get("sar_comments")
                                or "No Response Provided",
                                response_for=Role.get_status_as_string_by_id(user_type),
                                created_by=user,
                                user_role=user.current_role,
                            )
                            action_allowed = False
                            msg = "SAR updated successfully"
                            # security_resource_ids = get_notification_user_ids("security_resources",request_obj)
                            # if security_resource_ids:
                            #     extra_data = {
                            #         "comments": header_data.get("sar_comments") if header_data.get("sar_comments") else "",
                            #         "currentUser": user.get_full_name(),
                            #         "user_id": security_resource_ids,
                            #     }
                            #     common_email_notification(request_obj, "analyze_request", user, extra_data)
                        else:
                            new_status = RequestorTeam.STATUS_COMB_IPG_TEMPLATE_REVIEW
                            request_obj.status = new_status
                            request_obj.sub_status = (
                                RequestorTeam.SUB_STATUS_ISSUE_COMPLETED
                            )
                            if ato_status:
                                new_ato_status = int(ato_status)
                                old_ato_status = request_obj.ato_status
                                if str(new_ato_status) != str(old_ato_status):
                                    LogUpdate.objects.create(
                                        request=request_obj,
                                        event=LogUpdate.ATO_STATUS_EVENT,
                                        old_value=str(old_ato_status),
                                        new_value=str(new_ato_status),
                                        response_for="ATO Status",
                                        created_by=user,
                                        user_role=user.current_role,
                                    )
                                request_obj.ato_status = ato_status
                            request_obj.save()
    
                            LogUpdate.objects.create(
                                request=request_obj,
                                event=LogUpdate.STATUS_EVENT,
                                old_value=str(old_status),
                                new_value=str(new_status),
                                response_for=LogUpdate.RES_FOR_REQUEST,
                                created_by=user,
                                user_role=user.current_role,
                            )
                            LogUpdate.objects.create(
                                request=request_obj,
                                event=LogUpdate.SAR_LOG_EVENT,
                                old_value="-",
                                new_value=header_data.get("sar_comments")
                                or "No Response Provided",
                                response_for=Role.get_status_as_string_by_id(user_type),
                                created_by=user,
                                user_role=user.current_role,
                            )
                            action_allowed = False
                            msg = "SAR updated successfully"
                            # security_resource_ids = get_notification_user_ids("security_resources",request_obj)
                            # if security_resource_ids:
                            #     extra_data = {
                            #         "comments": header_data.get("sar_comments") if header_data.get("sar_comments") else "",
                            #         "currentUser": user.get_full_name(),
                            #         "user_id": security_resource_ids,
                            #     }
                            #     common_email_notification(request_obj, "analyze_request", user, extra_data)

                elif submit_id == "clearance_email_send":
                    if user_type in [
                        Role.ROLE_TYPE_AU,
                        Role.ROLE_TYPE_SECURITY_OFFICER,
                    ]:
                        action_allowed = True

                        try:
                            result = send_clearance_emails(
                                request_obj, user, ato_status
                            )

                            if not result.get("success", False):
                                return Response(
                                    {
                                        "status": False,
                                        "message": result.get("message", False),
                                        "errors": result.get("errors", False),
                                        "display_message": False,
                                        "data": [],
                                    },
                                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                )
                        except Exception as e:
                            return Response(
                                {
                                    "status": False,
                                    "message": str(e),
                                    "errors": ERRORS.get(
                                        "syntax_error_access", "Syntax Error"
                                    ),
                                    "display_message": True,
                                    "data": [],
                                },
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            )
                        publish_sar_on_leadership_approval(request_obj, user)

                if action_allowed:
                    if new_status != old_status:
                        request_obj.sub_status = new_status
                        request_obj.save()

                        LogUpdate.objects.create(
                            request=request_obj,
                            event=LogUpdate.STATUS_EVENT,
                            old_value=str(old_status),
                            new_value=str(new_status),
                            response_for=LogUpdate.RES_FOR_SUB_STATUS,
                            created_by=user,
                            user_role=user.current_role,
                        )

                    if email_extra:
                        common_email_notification(
                            request_obj, "analyze_request", user, email_extra
                        )
                    LogUpdate.objects.create(
                        request=request_obj,
                        event=LogUpdate.SAR_LOG_EVENT,
                        old_value="-",
                        new_value=header_data.get("sar_comments")
                        or "No Response Provided",
                        response_for=Role.get_status_as_string_by_id(user_type),
                        created_by=user,
                        user_role=user.current_role,
                    )

                    msg = "SAR updated successfully"

                return Response(
                    {
                        "status": True,
                        "display_message": False,
                        "message": msg,
                        "errors": [],
                        "data": [],
                    },
                    status=status.HTTP_200_OK,
                )

        except Exception as e:
            print(e)
            return Response(
                {
                    "status": False,
                    "message": ERRORS["syntax_error_access"],
                    "errors": [str(e)],
                    "display_message": True,
                    "data": [],
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
