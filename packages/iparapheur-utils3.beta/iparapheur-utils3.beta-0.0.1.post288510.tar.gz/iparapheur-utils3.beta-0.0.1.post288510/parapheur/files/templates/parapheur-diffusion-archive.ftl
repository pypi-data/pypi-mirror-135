<!DOCTYPE html>
<html><head><title>${document.properties['cm:title']}</title></head>
<body style="background-color: #f7f7f7; color: #000000"><div style="margin: 0pt; padding: 0pt;" dir="ltr"><table border="0" cellpadding="20" cellspacing="0" width="98%">
    <tbody><tr><td
            style="font-family: 'lucida grande',tahoma,verdana,arial,sans-serif; background-color: #f7f7f7" width="100%"><table border="0" cellpadding="0" cellspacing="0" width="620"><tbody>
    <tr><td style="padding: 4px 8px; background: rgb(59, 89, 152) none repeat scroll 0%; -moz-border-radius: 5px 5px 5px 5px; -moz-background-clip: border; -moz-background-origin: padding; -moz-background-inline-policy: continuous; color: rgb(255, 255, 255); font-weight: bold; font-family: 'lucida grande',tahoma,verdana,arial,sans-serif; vertical-align: middle; font-size: 16px; letter-spacing: -0.03em;
 text-align: left;">&nbsp; <i>i</i>-Parapheur</td>
    </tr>
    <tr><td><table style="font-family:Helvetica; color:#FFF; height:25px; border:0; margin:0; padding:0;" cellspacing="0" cellpadding="0"><tr>
        <td style="background-color:#CECECE; width:30px;">&nbsp;</td>
        <td style="text-align:center; background-color:#86858B; font-weight:bold; font-size:18px; padding-left:10px; padding-right:10px; width:590px;">
        ${document.properties['cm:title']}</td>
    </tr>
    </table></td>
    </tr>
    <tr><td style="border-left: 1px solid rgb(204, 204, 204); border-right: 1px solid rgb(204, 204, 204); border-bottom: 1px solid rgb(59, 89, 152); padding: 15px; background-color: rgb(255, 255, 255); font-family: 'lucida grande',tahoma,verdana,arial,sans-serif;" valign="top">
        <table width="100%"><tbody><tr><td style="font-size: 12px;" align="left" valign="top" width="100%">
            <div style="margin-bottom: 15px; font-size: 14px;">﻿Le dossier '${document.properties['cm:title']}' vient d'être archivé par ${person.properties.firstName}<#if person.properties.lastName?exists> ${person.properties.lastName}</#if>.</div>
            <div style="border-bottom: 1px solid rgb(204, 204, 204); line-height: 5px;">&nbsp;</div><br />
        </td></tr></tbody>
        </table>
    </td>
    </tr>
    <#if footer?? && footer!="" >
    <tr>
        <td  style="padding: 10px; color: rgb(153, 153, 153); font-size: 11px; font-family: 'lucida grande',tahoma,verdana,arial,sans-serif;">
        ${footer}
        </td>
    </tr>
    </#if>
    </tbody>
    </table></td></tr></tbody></table></div>
</body></html>
