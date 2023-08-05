<!DOCTYPE html>
<html lang="en">
<head>
    <meta http-equiv="content-type" content="text/html" charset="UTF-8"/>
    <title></title>
    <meta name="created" content="0;0"/>
    <meta name="changed" content="20080421;21344800"/>
    <style type="text/css">
        @page { size: 21cm 29.7cm }
        *{
            font-family: Arial, sans-serif;
            color: #262626;
        }

        div{
            display: inline-block;
        }

        h1{
            text-align: center;
        }

        h2{
            text-align: center;
            font-weight: 400;
        }

        table{
            width: 100%;
            border-collapse: collapse;
        }

        table.table td {
            padding: 10px 10px 10px 15px;
            height: 30px;
            border: 1px solid #dcdcdc;
            font-size: 18px;
        }

        p{
            font-size: 12px;
            font-weight: 500;
        }

        .table-head{
            background-color: #61c6ea;
            font-weight: bold;
            letter-spacing: 1px;
        }

        .focus{
            font-weight: bold;
        }
    </style>

</head>
<body lang="fr-FR" dir="ltr">
<div class="title">
    <table>
        <tr>
            <td width="15%">
                <img class="float" SRC="file:///opt/iParapheur/tomcat/shared/logo.png"
                     NAME="Logo" AliGN=LEFT WIDTH="auto" HEIGHT="80%" BORDER=0/>
            </td>
            <td width="70%">
                <h1>Bordereau de signature</h1>
                <h2>${dossier.properties['cm:title']}</h2>
            </td>
            <td width="15%"></td>
        </tr>
    </table>
</div>
<table class="table">
    <tr class="table-head">
        <td>Signataire</td>
        <td>Date</td>
        <td>Annotation</td>
    </tr>
	<#assign current_etape=0/>
	<#list etapes as etape>
		<tr>
            <td>
				<#if etape.signataire??>${etape.signataire}, ${etape.parapheurName}</#if>
            </td>
			<#if etape.dateValidation??>
				<td><#if etape.dateValidation??>${etape.dateValidation?string("dd/MM/yyyy")}</#if></td>
            <#else>
				<td class="table-head"></td>
            </#if>
            <td class="focus">
                <#if etape.actionDemandee??>
                    Action :
                    <#if etape.actionDemandee?lower_case == "archivage">
                        Fin de circuit
                    <#else>
                        ${etape.actionDemandee?lower_case?capitalize}
                    </#if>

                    <#if current_etape==etape_rejet>
                    <br/>
                    <span style="color: #d9534f">Dossier Rejeté</span>
                    </#if>

                </#if>
                <#if etape.annotation?? && etape.annotation?has_content><p>${etape.annotation?replace('\n','<br/>')}</p></#if>

                <#if etape.actionDemandee=="SIGNATURE" && etape.signature?has_content && etape.dateValidation??>
                      <br/><br/>
                      <p>
                                      <img SRC="file:///opt/iParapheur/tomcat/webapps/alfresco/images/parapheur/48px-app-certificate.jpg"
                                           NAME="Image3" AliGN=LEFT WIDTH=48 HEIGHT=48 BORDER=0/>
                    <#if etape.signature?starts_with("Certificat ")>${etape.signature}
                    <#else>
                        Certificat au nom de
                        <u>${etape.signataireCertInfos.subject_name}</u>
                        <#if etape.signataireCertInfos.organization?? && etape.signataireCertInfos.organization!="_incoonu_">
                                 (
                            <#if etape.signataireCertInfos.title?? && etape.signataireCertInfos.title!="_inconnu_">
                                ${etape.signataireCertInfos.title}
                                     ,
                            </#if>
                            ${etape.signataireCertInfos.organization})
                        </#if>,
                        &eacute;mis par <u>${etape.signataireCertInfos.issuer_name}</u>,
                        valide du ${etape.signataireCertInfos.certificate_valid_from}
                        au ${etape.signataireCertInfos.certificate_valid_to}.</p><br/>
                    </#if>
                </#if>
            </td>
        </tr>
        <#assign current_etape = current_etape + 1 />
    </#list>
</table>
<#if dossier.properties["{http://www.atolcd.com/alfresco/model/parapheur/1.0}typeMetier"]??>
    <p class="mentions">Dossier de type : ${dossier.properties["{http://www.atolcd.com/alfresco/model/parapheur/1.0}typeMetier"]}
        // ${dossier.properties["{http://www.atolcd.com/alfresco/model/parapheur/1.0}soustypeMetier"]}</p>
</#if>

<#if metadonnees?? && metadonnees?has_content>
<table>
    <tr>
        <td>
            <#setting locale="fr_FR"><#assign mdkeys = metadonnees?keys>
            Propri&eacute;t&eacute;s sp&eacute;cifiques :
        </td>
        <td>
            <ul><#list mdkeys as key><#if key?starts_with("DATE_B_")>
                <li> ${key?substring(7)} : ${metadonnees[key]?string("EEEEEEEE d MMMMM yyyy (yyyy-MM-dd)")}</li></#if>
            <#if key?starts_with("DOUBLE_")>
                <li> ${key?substring(7)} : ${metadonnees[key]?string(",##0.00")}</li></#if>
            <#if key?starts_with("INTEGER_")>
                <li> ${key?substring(8)} : ${metadonnees[key]?string(",##0")}</li></#if>
            <#if key?starts_with("STRING_")>
                <li> ${key?substring(7)} : ${metadonnees[key]}</li></#if>
            </#list></ul>
        </td>
    </tr>
</table>
</#if>

</body>
</html>
