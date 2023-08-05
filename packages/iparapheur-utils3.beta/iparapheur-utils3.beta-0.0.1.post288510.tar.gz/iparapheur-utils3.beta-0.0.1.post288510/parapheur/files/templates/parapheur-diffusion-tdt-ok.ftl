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
             <div style="margin-bottom: 15px; font-size: 14px;">﻿Le dossier '${document.properties['cm:title']}' a été télétransmis avec succès par ${person.properties.firstName}<#if person.properties.lastName?exists> ${person.properties.lastName}</#if>.</div>
             <div style="border-bottom: 1px solid rgb(204, 204, 204); line-height: 5px;">&nbsp;</div><br />
<#if annotation?? && annotation!="" && annotation!=" ">
             <div style="margin-bottom: 15px; font-size: 12px;">L'annotation suivante a été déposée : <span style=" font-size:14px">${annotation}</span></div>
             <div style="border-bottom: 1px solid rgb(204, 204, 204); line-height: 5px;">&nbsp;</div><br />
</#if>
             <div style="margin-bottom: 5px;">Vous pouvez y acc&eacute;der via le parapheur &eacute;lectronique :</div></td>
         </tr></tbody>
      </table><div style="padding-top: 10px;"><table cellpadding="0" cellspacing="0" width="100%"><tbody><tr>
          <td style="width: 50px;">&nbsp; </td>
          <td style="width: 90px;">&nbsp; </td>
          <td style="width: 200px;">&nbsp; </td>
          <td style="border: 1px solid rgb(255, 226, 34); padding: 10px; background-color: rgb(255, 248, 204); color: rgb(51, 51, 51); font-size: 11px; width: 200px;">
              <!-- div style="font-weight: bold; margin-bottom: 15px;">Vous avez un identifiant et un mot de passe&nbsp;:</div -->
              <center><table cellpadding="0" cellspacing="0"><tbody><tr>
                 <td style="border: 1px solid rgb(59, 110, 34); -moz-border-radius: 5px 5px 5px 5px"><table cellpadding="0" cellspacing="0"><tbody><tr>
                       <td style="border-top: 1px solid rgb(149, 191, 130); padding: 5px 5px; background-color: rgb(103, 165, 75); -moz-border-radius: 5px 5px 5px 5px"><a
<#if targetversion?? && targetversion!="" && targetversion!="3">
 href="${baseurl}/apercu?nodeId=${document.nodeRef}&fromMail=true"
<#else>
 href="${baseurl}/navigate/browse/${space.nodeRef.storeRef.protocol}/${space.nodeRef.storeRef.identifier}/${document.nodeRef.id}"
</#if>
 style="font-family: lucida grande,tahoma,verdana,arial,sans-serif; line-height: 1.4em;color: rgb(255, 255, 255); font-size: 14px; text-decoration: none;
  text-shadow: 0px 1px #efe589; display: block; padding: 3px 20px 4px; border-top: 0px solid #efe589; white-space: nowrap; -moz-border-radius: 5px 5px 5px 5px"
 target="_blank">Acc&eacute;der au dossier</a></td></tr></tbody>
                     </table></td></tr></tbody></table></center>
          </td>
          <td style="width: 30px;">&nbsp; </td>
        </tr></tbody>
      </table>
      </div>
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
