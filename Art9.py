from django.db import models
from django.conf import settings


class HighLevelData(models.Model):
    id = models.AutoField(primary_key=True)
    header_data = models.TextField(null=True, blank=True)
    request = models.ForeignKey(
        "RequestorTeam",
        on_delete=models.CASCADE,
        db_column="sgp_id",
        to_field="sgp_id",
        related_name="high_level_data",
        null=True,
        blank=True,
    )
    comment = models.TextField(null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    is_active = models.IntegerField(default=1, db_index=True)

    class Meta:
        db_table = "high_level_data"
        indexes = [
            models.Index(fields=["request", "is_active"]),
            models.Index(
                fields=[
                    "request",
                    "is_active",
                    "-created_date",
                ]
            ),
        ]

    def get_processed_header_data(self):
        if not self.header_data:
            return self.header_data
        app_url = settings.DOMAIN_URL
        value = self.header_data
        replacements = {
            "/kpmgivtm/public/img/first_page_side.png": f"{app_url}/backend/img/first_page_side.png",
            "/kpmgivtm/public/img/first_page_sar.png": f"{app_url}/backend/img/first_page_sar.jpg",
            "/kpmgivtm/public/img/first_page_sar.jpg": f"{app_url}/backend/img/first_page_sar.jpg",
            "https://abc.kworld.abc.com/abcivtm/public/storage/result_storage/architecture_img": f"{app_url}/backend/result_storage/architecture_img",
            "/kpmgivtm/public/storage/result_storage/architecture_img": f"{app_url}/backend/result_storage/architecture_img",
            "/kpmgivtm/public/img/logo_new.png": f"{app_url}/backend/img/logo_new.png",
        }
        for old_path, new_path in replacements.items():
            value = value.replace(old_path, new_path)
        return value


header_data
<div style="max-width: 83% !important;margin-left: auto;margin-right: auto;">
     <div>
         <table class="table table-bordered">
             <thead>
                 <tr>
                     <th style="color:white;" colspan="4">Governance and Strategy</th>
                 </tr>
                 <tr>
                     <th style="width: 24%;" class="bg-info">Security Requirement</th>
                     <th style="width: 30%;" class="bg-info">Implementation Details</th>
                     <th style="width: 20%;" class="bg-info">Status</th>
                     <th class="bg-info">Comment</th>
                 </tr>
             </thead>
             <tbody>
                 <tr>
                     <td><b>Certification (ISO, SOC2, etc.)</b></td>
                     <td>[Statement on how the solution implements the requirement]</td>
                     <td><div class="header_3_4_security_value">-</div><div class="header_3_4_security_status"><select class="w-full border border-gray-300 rounded-md p-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 header_security_status"><option value="0">Select Status</option><option value="1" style="background-color:#A8D08D">Implemented</option><option value="2" style="background-color:#FFE599">Partially Implemented</option><option value="3" style="background-color:#F4B083">Gap</option><option value="4" style="background-color:#D0CECE">Not Assessed</option><option value="5" style="background-color:#FFFFFF">Not Applicable</option></select></div></td>
                     <td>-<br></td>
                 </tr>
             </tbody>
         </table>
     </div>
     <br>
     <div>
         <table class="table table-bordered">
             <thead>
                 <tr>
                     <th style="color:white;" colspan="4">Posture and Vulnerability Management</th>
                 </tr>
                 <tr>
                     <th style="width: 24%;" class="bg-info">Security Requirement</th>
                     <th style="width: 30%;" class="bg-info">Implementation Details</th>
                     <th style="width: 20%;" class="bg-info">Status</th>
                     <th class="bg-info">Comment</th>
                 </tr>
             </thead>
             <tbody>
                 <tr>
                     <td><b>System Hardening</b></td>
                     <td>[Statement on how the solution implements the requirement]</td>
                     <td><div class="header_3_4_security_value">-</div><div class="header_3_4_security_status"><select class="w-full border border-gray-300 rounded-md p-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 header_security_status"><option value="0">Select Status</option><option value="1" style="background-color:#A8D08D">Implemented</option><option value="2" style="background-color:#FFE599">Partially Implemented</option><option value="3" style="background-color:#F4B083">Gap</option><option value="4" style="background-color:#D0CECE">Not Assessed</option><option value="5" style="background-color:#FFFFFF">Not Applicable</option></select></div></td>
                     <td>-<br></td>
                 </tr>
                 <tr>
                     <td><b>Application Patching</b><h6>Explain the responsible party (individual, a distribution list, organization, etc.) and how they will maintain application patching on an on-going basis</h6></td>
                     <td>[Statement on how the solution implements the requirement]</td>
                     <td><div class="header_3_4_security_value">-</div><div class="header_3_4_security_status"><select class="w-full border border-gray-300 rounded-md p-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 header_security_status"><option value="0">Select Status</option><option value="1" style="background-color:#A8D08D">Implemented</option><option value="2" style="background-color:#FFE599">Partially Implemented</option><option value="3" style="background-color:#F4B083">Gap</option><option value="4" style="background-color:#D0CECE">Not Assessed</option><option value="5" style="background-color:#FFFFFF">Not Applicable</option></select></div></td>
                     <td>-<br></td>
                 </tr>
             </tbody>
         </table>
     </div>
     <br>
     <div>
         <table class="table table-bordered">
             <thead>
                 <tr>
                     <th style="color:white;" colspan="4">Identity Management</th>
                 </tr>
                 <tr>
                     <th style="width: 24%;" class="bg-info">Security Requirement</th>
                     <th style="width: 30%;" class="bg-info">Implementation Details</th>
                     <th style="width: 20%;" class="bg-info">Status</th>
                     <th class="bg-info">Comment</th>
                 </tr>
             </thead>
             <tbody>
                 <tr>
                     <td><b>Authentication</b></td>
                     <td>[Statement on how the solution implements the requirement]</td>
                     <td><div class="header_3_4_security_value">-</div><div class="header_3_4_security_status"><select class="w-full border border-gray-300 rounded-md p-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 header_security_status"><option value="0">Select Status</option><option value="1" style="background-color:#A8D08D">Implemented</option><option value="2" style="background-color:#FFE599">Partially Implemented</option><option value="3" style="background-color:#F4B083">Gap</option><option value="4" style="background-color:#D0CECE">Not Assessed</option><option value="5" style="background-color:#FFFFFF">Not Applicable</option></select></div></td>
                     <td>-<br></td>
                 </tr>
                 <tr>
                     <td><b>Authorization</b></td>
                     <td>[Statement on how the solution implements the requirement]</td>
                     <td><div class="header_3_4_security_value">-</div><div class="header_3_4_security_status"><select class="w-full border border-gray-300 rounded-md p-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 header_security_status"><option value="0">Select Status</option><option value="1" style="background-color:#A8D08D">Implemented</option><option value="2" style="background-color:#FFE599">Partially Implemented</option><option value="3" style="background-color:#F4B083">Gap</option><option value="4" style="background-color:#D0CECE">Not Assessed</option><option value="5" style="background-color:#FFFFFF">Not Applicable</option></select></div></td>
                     <td>-<br></td>
                 </tr>
                 <tr>
                     <td><b>Information (Data) Workflow</b></td>
                     <td>[Statement on how the solution implements the requirement]</td>
                     <td><div class="header_3_4_security_value">-</div><div class="header_3_4_security_status"><select class="w-full border border-gray-300 rounded-md p-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 header_security_status"><option value="0">Select Status</option><option value="1" style="background-color:#A8D08D">Implemented</option><option value="2" style="background-color:#FFE599">Partially Implemented</option><option value="3" style="background-color:#F4B083">Gap</option><option value="4" style="background-color:#D0CECE">Not Assessed</option><option value="5" style="background-color:#FFFFFF">Not Applicable</option></select></div></td>
                     <td>-<br></td>
                 </tr>
                 <tr>
                     <td><b>Session Management</b></td>
                     <td>[Statement on how the solution implements the requirement]</td>
                     <td><div class="header_3_4_security_value">-</div><div class="header_3_4_security_status"><select class="w-full border border-gray-300 rounded-md p-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 header_security_status"><option value="0">Select Status</option><option value="1" style="background-color:#A8D08D">Implemented</option><option value="2" style="background-color:#FFE599">Partially Implemented</option><option value="3" style="background-color:#F4B083">Gap</option><option value="4" style="background-color:#D0CECE">Not Assessed</option><option value="5" style="background-color:#FFFFFF">Not Applicable</option></select></div></td>
                     <td>-<br></td>
                 </tr>
                 <tr>
                     <td><b>Segregation of Duties</b></td>
                     <td>[Statement on how the solution implements the requirement]</td>
                     <td><div class="header_3_4_security_value">-</div><div class="header_3_4_security_status"><select class="w-full border border-gray-300 rounded-md p-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 header_security_status"><option value="0">Select Status</option><option value="1" style="background-color:#A8D08D">Implemented</option><option value="2" style="background-color:#FFE599">Partially Implemented</option><option value="3" style="background-color:#F4B083">Gap</option><option value="4" style="background-color:#D0CECE">Not Assessed</option><option value="5" style="background-color:#FFFFFF">Not Applicable</option></select></div></td>
                     <td>-<br></td>
                 </tr>
                 <tr>
                     <td><b>Role Based Access Control (RBAC)</b></td>
                     <td>[Statement on how the solution implements the requirement]</td>
                     <td><div class="header_3_4_security_value">-</div><div class="header_3_4_security_status"><select class="w-full border border-gray-300 rounded-md p-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 header_security_status"><option value="0">Select Status</option><option value="1" style="background-color:#A8D08D">Implemented</option><option value="2" style="background-color:#FFE599">Partially Implemented</option><option value="3" style="background-color:#F4B083">Gap</option><option value="4" style="background-color:#D0CECE">Not Assessed</option><option value="5" style="background-color:#FFFFFF">Not Applicable</option></select></div></td>
                     <td>-<br></td>
                 </tr>
             </tbody>
         </table>
     </div>
     <br>
     <div>
         <table class="table table-bordered">
             <thead>
                 <tr>
                     <th style="color:white;" colspan="4">Privilege Access</th>
                 </tr>
                 <tr>
                     <th style="width: 24%;" class="bg-info">Security Requirement</th>
                     <th style="width: 30%;" class="bg-info">Implementation Details</th>
                     <th style="width: 20%;" class="bg-info">Status</th>
                     <th class="bg-info">Comment</th>
                 </tr>
             </thead>
             <tbody>
                 <tr>
                     <td><b>Privileged Access Management</b></td>
                     <td>[Statement on how the solution implements the requirement]</td>
                     <td><div class="header_3_4_security_value">-</div><div class="header_3_4_security_status"><select class="w-full border border-gray-300 rounded-md p-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 header_security_status"><option value="0">Select Status</option><option value="1" style="background-color:#A8D08D">Implemented</option><option value="2" style="background-color:#FFE599">Partially Implemented</option><option value="3" style="background-color:#F4B083">Gap</option><option value="4" style="background-color:#D0CECE">Not Assessed</option><option value="5" style="background-color:#FFFFFF">Not Applicable</option></select></div></td>
                     <td>-<br></td>
                 </tr>
             </tbody>
         </table>
     </div>
     <br>
     <div>
         <table class="table table-bordered">
             <thead>
                 <tr>
                     <th style="color:white;" colspan="4">Endpoint Security</th>
                 </tr>
                 <tr>
                     <th style="width: 24%;" class="bg-info">Security Requirement</th>
                     <th style="width: 30%;" class="bg-info">Implementation Details</th>
                     <th style="width: 20%;" class="bg-info">Status</th>
                     <th class="bg-info">Comment</th>
                 </tr>
             </thead>
             <tbody>
                 <tr>
                     <td><b>Antivirus &amp; Host-based Security</b></td>
                     <td>[Statement on how the solution implements the requirement]</td>
                     <td><div class="header_3_4_security_value">-</div><div class="header_3_4_security_status"><select class="w-full border border-gray-300 rounded-md p-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 header_security_status"><option value="0">Select Status</option><option value="1" style="background-color:#A8D08D">Implemented</option><option value="2" style="background-color:#FFE599">Partially Implemented</option><option value="3" style="background-color:#F4B083">Gap</option><option value="4" style="background-color:#D0CECE">Not Assessed</option><option value="5" style="background-color:#FFFFFF">Not Applicable</option></select></div></td>
                     <td>-<br></td>
                 </tr>
             </tbody>
         </table>
     </div>
     <br>
     <div>
         <table class="table table-bordered">
             <thead>
                 <tr>
                     <th style="color:white;" colspan="4">Network Security</th>
                 </tr>
                 <tr>
                     <th style="width: 24%;" class="bg-info">Security Requirement</th>
                     <th style="width: 30%;" class="bg-info">Implementation Details</th>
                     <th style="width: 20%;" class="bg-info">Status</th>
                     <th class="bg-info">Comment</th>
                 </tr>
             </thead>
             <tbody>
                 <tr>
                     <td><b>Logical &amp; Physical Segmentation</b></td>
                     <td>[Statement on how the solution implements the requirement]</td>
                     <td><div class="header_3_4_security_value">-</div><div class="header_3_4_security_status"><select class="w-full border border-gray-300 rounded-md p-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 header_security_status"><option value="0">Select Status</option><option value="1" style="background-color:#A8D08D">Implemented</option><option value="2" style="background-color:#FFE599">Partially Implemented</option><option value="3" style="background-color:#F4B083">Gap</option><option value="4" style="background-color:#D0CECE">Not Assessed</option><option value="5" style="background-color:#FFFFFF">Not Applicable</option></select></div></td>
                     <td>-<br></td>
                 </tr>
                 <tr>
                     <td><b>Network-based Security</b><h6>Intrusion Detection / Prevention Systems, Proxy, Web Application Firewall, Azure Network Security Group (NSG), including NSG rules</h6></td>
                     <td>[Statement on how the solution implements the requirement]</td>
                     <td><div class="header_3_4_security_value">-</div><div class="header_3_4_security_status"><select class="w-full border border-gray-300 rounded-md p-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 header_security_status"><option value="0">Select Status</option><option value="1" style="background-color:#A8D08D">Implemented</option><option value="2" style="background-color:#FFE599">Partially Implemented</option><option value="3" style="background-color:#F4B083">Gap</option><option value="4" style="background-color:#D0CECE">Not Assessed</option><option value="5" style="background-color:#FFFFFF">Not Applicable</option></select></div></td>
                     <td>-<br></td>
                 </tr>
             </tbody>
         </table>
     </div>
     <br>
     <div>
         <table class="table table-bordered">
             <thead>
                 <tr>
                     <th style="color:white;" colspan="4">DevOps Security</th>
                 </tr>
                 <tr>
                     <th style="width: 24%;" class="bg-info">Security Requirement</th>
                     <th style="width: 30%;" class="bg-info">Implementation Details</th>
                     <th style="width: 20%;" class="bg-info">Status</th>
                     <th class="bg-info">Comment</th>
                 </tr>
             </thead>
             <tbody>
                 <tr>
                     <td><b>Static Code Analysis</b></td>
                     <td>[Statement on how the solution implements the requirement]</td>
                     <td><div class="header_3_4_security_value">-</div><div class="header_3_4_security_status"><select class="w-full border border-gray-300 rounded-md p-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 header_security_status"><option value="0">Select Status</option><option value="1" style="background-color:#A8D08D">Implemented</option><option value="2" style="background-color:#FFE599">Partially Implemented</option><option value="3" style="background-color:#F4B083">Gap</option><option value="4" style="background-color:#D0CECE">Not Assessed</option><option value="5" style="background-color:#FFFFFF">Not Applicable</option></select></div></td>
                     <td>-<br></td>
                 </tr>
                 <tr>
                     <td><b>Dynamic Code Analysis</b></td>
                     <td>[Statement on how the solution implements the requirement]</td>
                     <td><div class="header_3_4_security_value">-</div><div class="header_3_4_security_status"><select class="w-full border border-gray-300 rounded-md p-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 header_security_status"><option value="0">Select Status</option><option value="1" style="background-color:#A8D08D">Implemented</option><option value="2" style="background-color:#FFE599">Partially Implemented</option><option value="3" style="background-color:#F4B083">Gap</option><option value="4" style="background-color:#D0CECE">Not Assessed</option><option value="5" style="background-color:#FFFFFF">Not Applicable</option></select></div></td>
                     <td>-<br></td>
                 </tr>
                 <tr>
                     <td><b>Penetration Testing</b></td>
                     <td>[Statement on how the solution implements the requirement]</td>
                     <td><div class="header_3_4_security_value">-</div><div class="header_3_4_security_status"><select class="w-full border border-gray-300 rounded-md p-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 header_security_status"><option value="0">Select Status</option><option value="1" style="background-color:#A8D08D">Implemented</option><option value="2" style="background-color:#FFE599">Partially Implemented</option><option value="3" style="background-color:#F4B083">Gap</option><option value="4" style="background-color:#D0CECE">Not Assessed</option><option value="5" style="background-color:#FFFFFF">Not Applicable</option></select></div></td>
                     <td>-<br></td>
                 </tr>
             </tbody>
         </table>
     </div>
     <br>
     <div>
         <table class="table table-bordered">
             <thead>
                 <tr>
                     <th style="color:white;" colspan="4">Data Protection</th>
                 </tr>
                 <tr>
                     <th style="width: 24%;" class="bg-info">Security Requirement</th>
                     <th style="width: 30%;" class="bg-info">Implementation Details</th>
                     <th style="width: 20%;" class="bg-info">Status</th>
                     <th class="bg-info">Comment</th>
                 </tr>
             </thead>
             <tbody>
                 <tr>
                     <td><b>Data-in-Transit</b></td>
                     <td>[Statement on how the solution implements the requirement]</td>
                     <td><div class="header_3_4_security_value">-</div><div class="header_3_4_security_status"><select class="w-full border border-gray-300 rounded-md p-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 header_security_status"><option value="0">Select Status</option><option value="1" style="background-color:#A8D08D">Implemented</option><option value="2" style="background-color:#FFE599">Partially Implemented</option><option value="3" style="background-color:#F4B083">Gap</option><option value="4" style="background-color:#D0CECE">Not Assessed</option><option value="5" style="background-color:#FFFFFF">Not Applicable</option></select></div></td>
                     <td>-<br></td>
                 </tr>
                 <tr>
                     <td><b>Data-at-Rest</b></td>
                     <td>[Statement on how the solution implements the requirement]</td>
                     <td><div class="header_3_4_security_value">-</div><div class="header_3_4_security_status"><select class="w-full border border-gray-300 rounded-md p-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 header_security_status"><option value="0">Select Status</option><option value="1" style="background-color:#A8D08D">Implemented</option><option value="2" style="background-color:#FFE599">Partially Implemented</option><option value="3" style="background-color:#F4B083">Gap</option><option value="4" style="background-color:#D0CECE">Not Assessed</option><option value="5" style="background-color:#FFFFFF">Not Applicable</option></select></div></td>
                     <td>-<br></td>
                 </tr>
                 <tr>
                     <td><b>Database Encryption</b></td>
                     <td>[Statement on how the solution implements the requirement]</td>
                     <td><div class="header_3_4_security_value">-</div><div class="header_3_4_security_status"><select class="w-full border border-gray-300 rounded-md p-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 header_security_status"><option value="0">Select Status</option><option value="1" style="background-color:#A8D08D">Implemented</option><option value="2" style="background-color:#FFE599">Partially Implemented</option><option value="3" style="background-color:#F4B083">Gap</option><option value="4" style="background-color:#D0CECE">Not Assessed</option><option value="5" style="background-color:#FFFFFF">Not Applicable</option></select></div></td>
                     <td>-<br></td>
                 </tr>
                 <tr>
                     <td><b>Key Management</b></td>
                     <td>[Statement on how the solution implements the requirement]</td>
                     <td><div class="header_3_4_security_value">-</div><div class="header_3_4_security_status"><select class="w-full border border-gray-300 rounded-md p-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 header_security_status"><option value="0">Select Status</option><option value="1" style="background-color:#A8D08D">Implemented</option><option value="2" style="background-color:#FFE599">Partially Implemented</option><option value="3" style="background-color:#F4B083">Gap</option><option value="4" style="background-color:#D0CECE">Not Assessed</option><option value="5" style="background-color:#FFFFFF">Not Applicable</option></select></div></td>
                     <td>-<br></td>
                 </tr>
                 <tr>
                     <td><b>Reporting / Data Exporting</b></td>
                     <td>[Statement on how the solution implements the requirement]</td>
                     <td><div class="header_3_4_security_value">-</div><div class="header_3_4_security_status"><select class="w-full border border-gray-300 rounded-md p-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 header_security_status"><option value="0">Select Status</option><option value="1" style="background-color:#A8D08D">Implemented</option><option value="2" style="background-color:#FFE599">Partially Implemented</option><option value="3" style="background-color:#F4B083">Gap</option><option value="4" style="background-color:#D0CECE">Not Assessed</option><option value="5" style="background-color:#FFFFFF">Not Applicable</option></select></div></td>
                     <td>-<br></td>
                 </tr>
                 <tr>
                     <td><b>External Content</b><h6>Provide summary details of any external data providers transferring content to the system and the provider's location and communications method(s).</h6></td>
                     <td>[Statement on how the solution implements the requirement]</td>
                     <td><div class="header_3_4_security_value">-</div><div class="header_3_4_security_status"><select class="w-full border border-gray-300 rounded-md p-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 header_security_status"><option value="0">Select Status</option><option value="1" style="background-color:#A8D08D">Implemented</option><option value="2" style="background-color:#FFE599">Partially Implemented</option><option value="3" style="background-color:#F4B083">Gap</option><option value="4" style="background-color:#D0CECE">Not Assessed</option><option value="5" style="background-color:#FFFFFF">Not Applicable</option></select></div></td>
                     <td>-<br></td>
                 </tr>
             </tbody>
         </table>
     </div>
     <br>
     <div>
         <table class="table table-bordered">
             <thead>
                 <tr>
                     <th style="color:white;" colspan="4">Backup and Recovery</th>
                 </tr>
                 <tr>
                     <th style="width: 24%;" class="bg-info">Security Requirement</th>
                     <th style="width: 30%;" class="bg-info">Implementation Details</th>
                     <th style="width: 20%;" class="bg-info">Status</th>
                     <th class="bg-info">Comment</th>
                 </tr>
             </thead>
             <tbody>
                 <tr>
                     <td><b>Backup / Disaster Recovery</b><h6>VM Snapshot, Microsoft Azure Recovery Service (MAR) agent, Azure Backup Server, etc.</h6></td>
                     <td>[Statement on how the solution implements the requirement with alignment to the BC level]</td>
                     <td><div class="header_3_4_security_value">-</div><div class="header_3_4_security_status"><select class="w-full border border-gray-300 rounded-md p-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 header_security_status"><option value="0">Select Status</option><option value="1" style="background-color:#A8D08D">Implemented</option><option value="2" style="background-color:#FFE599">Partially Implemented</option><option value="3" style="background-color:#F4B083">Gap</option><option value="4" style="background-color:#D0CECE">Not Assessed</option><option value="5" style="background-color:#FFFFFF">Not Applicable</option></select></div></td>
                     <td>-<br></td>
                 </tr>
                 <tr>
                     <td><b>Fault Tolerance</b><h6>(Sustain availability, DDoS mitigation, etc.)</h6></td>
                     <td>[Statement on how the solution implements the requirement with alignment to the BC level]</td>
                     <td><div class="header_3_4_security_value">-</div><div class="header_3_4_security_status"><select class="w-full border border-gray-300 rounded-md p-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 header_security_status"><option value="0">Select Status</option><option value="1" style="background-color:#A8D08D">Implemented</option><option value="2" style="background-color:#FFE599">Partially Implemented</option><option value="3" style="background-color:#F4B083">Gap</option><option value="4" style="background-color:#D0CECE">Not Assessed</option><option value="5" style="background-color:#FFFFFF">Not Applicable</option></select></div></td>
                     <td>-<br></td>
                 </tr>
                 <tr>
                     <td><b>Redundancy</b><h6>Specify if geo-redundancy has been requested and describe its implementation.</h6></td>
                     <td>[Statement on how the solution implements the requirement with alignment to the BC level]</td>
                     <td><div class="header_3_4_security_value">-</div><div class="header_3_4_security_status"><select class="w-full border border-gray-300 rounded-md p-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 header_security_status"><option value="0">Select Status</option><option value="1" style="background-color:#A8D08D">Implemented</option><option value="2" style="background-color:#FFE599">Partially Implemented</option><option value="3" style="background-color:#F4B083">Gap</option><option value="4" style="background-color:#D0CECE">Not Assessed</option><option value="5" style="background-color:#FFFFFF">Not Applicable</option></select></div></td>
                     <td>-<br></td>
                 </tr>
                 <tr>
                     <td><b>Incident Management (Application)</b></td>
                     <td>[Statement on how the solution implements the requirement with alignment to the BC level]</td>
                     <td><div class="header_3_4_security_value">-</div><div class="header_3_4_security_status"><select class="w-full border border-gray-300 rounded-md p-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 header_security_status"><option value="0">Select Status</option><option value="1" style="background-color:#A8D08D">Implemented</option><option value="2" style="background-color:#FFE599">Partially Implemented</option><option value="3" style="background-color:#F4B083">Gap</option><option value="4" style="background-color:#D0CECE">Not Assessed</option><option value="5" style="background-color:#FFFFFF">Not Applicable</option></select></div></td>
                     <td>-<br></td>
                 </tr>
             </tbody>
         </table>
     </div>
     <br>
     <div>
         <table class="table table-bordered">
             <thead>
                 <tr>
                     <th style="color:white;" colspan="4">Logging &amp; Threat Detection</th>
                 </tr>
                 <tr>
                     <th style="width: 24%;" class="bg-info">Security Requirement</th>
                     <th style="width: 30%;" class="bg-info">Implementation Details</th>
                     <th style="width: 20%;" class="bg-info">Status</th>
                     <th class="bg-info">Comment</th>
                 </tr>
             </thead>
             <tbody>
                 <tr>
                     <td><b>Application Monitoring</b><h6>Database, Frontend (IIS), Transactions (accesses, changes, etc.), Performance, etc.</h6></td>
                     <td>[Statement on how the solution implements the requirement]</td>
                     <td><div class="header_3_4_security_value">-</div><div class="header_3_4_security_status"><select class="w-full border border-gray-300 rounded-md p-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 header_security_status"><option value="0">Select Status</option><option value="1" style="background-color:#A8D08D">Implemented</option><option value="2" style="background-color:#FFE599">Partially Implemented</option><option value="3" style="background-color:#F4B083">Gap</option><option value="4" style="background-color:#D0CECE">Not Assessed</option><option value="5" style="background-color:#FFFFFF">Not Applicable</option></select></div></td>
                     <td>-<br></td>
                 </tr>
                 <tr>
                     <td><b>System Monitoring</b><h6>Operating System, Host-based Protections, Host Performance, etc.</h6></td>
                     <td>[Statement on how the solution implements the requirement]</td>
                     <td><div class="header_3_4_security_value">-</div><div class="header_3_4_security_status"><select class="w-full border border-gray-300 rounded-md p-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 header_security_status"><option value="0">Select Status</option><option value="1" style="background-color:#A8D08D">Implemented</option><option value="2" style="background-color:#FFE599">Partially Implemented</option><option value="3" style="background-color:#F4B083">Gap</option><option value="4" style="background-color:#D0CECE">Not Assessed</option><option value="5" style="background-color:#FFFFFF">Not Applicable</option></select></div></td>
                     <td>-<br></td>
                 </tr>
                 <tr>
                     <td><b>Infrastructure Monitoring</b><h6>Intrusion Detection / Prevention Systems, Proxy, Web Application Firewall, Azure Network Security Group (NSG), NSG policy, etc.</h6></td>
                     <td>[Statement on how the solution implements the requirement]</td>
                     <td><div class="header_3_4_security_value">-</div><div class="header_3_4_security_status"><select class="w-full border border-gray-300 rounded-md p-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 header_security_status"><option value="0">Select Status</option><option value="1" style="background-color:#A8D08D">Implemented</option><option value="2" style="background-color:#FFE599">Partially Implemented</option><option value="3" style="background-color:#F4B083">Gap</option><option value="4" style="background-color:#D0CECE">Not Assessed</option><option value="5" style="background-color:#FFFFFF">Not Applicable</option></select></div></td>
                     <td>-<br></td>
                 </tr>
                 <tr>
                     <td><b>Log Retention Time</b></td>
                     <td>[Statement of time for each log type, if different. If retention time is less than 180 days note as a Gap]</td>
                     <td><div class="header_3_4_security_value">-</div><div class="header_3_4_security_status"><select class="w-full border border-gray-300 rounded-md p-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 header_security_status"><option value="0">Select Status</option><option value="1" style="background-color:#A8D08D">Implemented</option><option value="2" style="background-color:#FFE599">Partially Implemented</option><option value="3" style="background-color:#F4B083">Gap</option><option value="4" style="background-color:#D0CECE">Not Assessed</option><option value="5" style="background-color:#FFFFFF">Not Applicable</option></select></div></td>
                     <td>-<br></td>
                 </tr>
             </tbody>
         </table>
     </div>
   </div>


