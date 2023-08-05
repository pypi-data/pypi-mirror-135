<!DOCTYPE html>
<html>
<head>
    <title>e-mail recapitulatif</title>

    <style type="text/css">

        body {
            margin: 0;
            display: block;
            position: relative;
            font-family: "Helvetica Neue",Helvetica,Arial,sans-serif;
            font-size: 14px;
            line-height: 1.42857143;
            color: #333;
            background-color: #fff;
            word-wrap: break-word;
        }
        h1, h2, h3 {
            margin-top: 20px;
            margin-bottom: 10px;
            font-family: inherit;
            font-weight: 500;
            line-height: 1.1;
            color: inherit;
        }
        h1 {
            font-size: 20px;
        }
        h2 {
            font-size: 18px;
        }
        h1 small, h2 small, h3 small {
            font-size: 65%;
            font-weight: 400;
            line-height: 1;
            color: #999;
        }
        div {
            display: block;
        }
        p {
            margin: 0 0 10px;
        }
        a {
            text-decoration:none;
            color:black;
        }
        .container {
            width: 920px;
            margin-right: auto;
            margin-left: auto;
            padding-left: 15px;
            padding-right: 15px;
        }
        .well {
            min-height: 20px;
            padding: 19px;
            margin-bottom: 20px;
            background-color: #f5f5f5;
            border: 1px solid #e3e3e3;
            border-radius: 4px;
        }
        .bg-primary {
            background-color: #428bca;
        }
        .lead {
            margin-bottom: 20px;
            font-size: 16px;
            font-weight: 200;
            line-height: 1.4;
        }
        .btn-success {
            color: #fff;
            background-color: #5cb85c;
            border-color: #4cae4c;
        }

        .btn {
            display: inline-block;
            margin-bottom: 0;
            font-weight: 400;
            text-align: center;
            vertical-align: middle;
            cursor: pointer;
            background-image: none;
            border: 1px solid transparent;
            white-space: nowrap;
            padding: 6px 12px;
            font-size: 16px;
            line-height: 1.42857143;
            border-radius: 4px;
            text-transform: none;
        }

        .table {
            width: 100%;
            margin-bottom: 20px;
            border-collapse: collapse;
            border-spacing: 0;
            display: table;
        }
        .table-bordered {
            border: 1px solid #ddd;
        }

        .table-striped>tbody>tr:nth-child(odd)>td, .table-striped>tbody>tr:nth-child(odd)>th {
            background-color: #f9f9f9;
        }

        .right {
            float:right;
        }

        #btn {
            display: inline-block;
            margin-bottom: 0;
            font-weight: 400;
            text-align: center;
            vertical-align: middle;
            cursor: pointer;
            background-image: none;
            border: 1px solid transparent;
            white-space: nowrap;
            padding: 6px 12px;
            font-size: 16px;
            line-height: 1.42857143;
            border-radius: 4px;
            text-transform: none;
            color: #fff;
            background-color: #5cb85c;
            border-color: #4cae4c;
        }
    </style>
</head>
<body>

<div class="container">

    <h1 class="bg-primary" style="color:white; padding-left:15px">
        <i>i</i>-Parapheur | e-mail recapitulatif
    </h1>
    <div>

        <#list notificationsMap?keys?sort as rootKey><!-- Liste des bureaux -->

        <div class="well">
            <h2>${rootKey}</h2>

            <#list notificationsMap[rootKey]?keys?sort as key><!-- Liste des dossiers -->



                <#assign first = true>
                <#assign haslate = false>
                <#list notificationsMap[rootKey][key] as notification><!-- Liste des notifications pour un dossier -->

                    <#if first == true>

                        <span class="lead">
                            <#if notification.getPayload()["dossierName"]??>
                                ${notification.getPayload()["dossierName"]}
                            </#if>
                        </span>
                        <span id="btn" class="btn btn-success right">
                            <#if notification.getPayload()["id"]??>
                            <a href="${url}${notification.getPayload()["id"]}" target="_blank">
                            <#else>
                            <a href="${url}${notification.getPayload()["nodeRef"].id}" target="_blank">
                            </#if>
                                Acc&eacute;der au dossier
                            </a>
                        </span>

                        <table class="table table-bordered table-striped">
                        <thead>
                            <tr>
                                <th align="left">Date</th>
                                <th align="left">Acteur</th>
                                <th align="left">Action</th>
                                <th align="left">Annotation</th>
                            </tr>
                        </thead>
                        <tbody>

                    </#if>

                    <#if notification.getPayload()?? && !(notification.getPayload()["reason"]?? && notification.getPayload()["reason"] == "retard" && haslate)>
                        <tr>
                            <td>
                                ${timestamp.number_to_datetime(notification.getTimestamp())}
                            </td>
                            <td>
                                <#if notification.getPayload()["nomValideur"]??>${notification.getPayload()["nomValideur"]}</#if>
                                <#if notification.getPayload()["nomParapheurValideur"]??> (${notification.getPayload()["nomParapheurValideur"]})</#if>
                            </td>

                            <td>
                            <#if notification.getPayload()["reason"]??>
                                <#switch notification.getPayload()["reason"]>
                                    <#case "approve">
                                        <#if notification.getPayload()["target"]?? && notification.getPayload()["target"] == "diff">
                                            ${notification.getActionEffectuee()}
                                        <#else>
                                            Déposé pour ${notification.getActionDemandee()}
                                        </#if>
                                        <#break>
                                    <#case "reject">
                                        <#if notification.getPayload()["target"]?? && notification.getPayload()["target"] == "current">
                                            Déposé sur le bureau après un rejet
                                        <#else>
                                            Dossier rejeté
                                        </#if>
                                        <#break>
                                    <#case "remord">
                                        Droit de remords sur le dossier
                                        <#break>
                                    <#case "reviewing">
                                        <#if notification.getPayload()["target"]?? && (notification.getPayload()["target"] == "secretariat")>
                                            Dossier envoyé au secretariat pour relecture
                                        <#else>
                                            Dossier renvoyé par le secretariat après relecture
                                        </#if>
                                        <#break>
                                    <#case "retard">
                                        <#assign haslate = true>
                                        <span style="color: red;">&#9888; Dossier en retard</span>
                                        <#break>
                                    <#default>
                                        Action sur le dossier.
                                </#switch>
                            </#if>
                            </td>

                            <td>
                                <#if notification.getPayload()["annotationPublique"]??>${notification.getPayload()["annotationPublique"]}</#if>
                            </td>
                        </tr>

                    </#if>
                    <#assign first = false>
                </#list>
                    </tbody>
                </table>
             </#list>
            </div>
        </#list>
    </div>


<#if footer?? && footer!="" >
    <p>
        <small>${footer}</small>
    </p>
</#if>
</div>
</body>
</html>
