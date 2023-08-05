<!DOCTYPE html>
<html>
<head>
    <title>${dossierName}</title>

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
        .container {
            width: 620px;
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

    </style>
</head>

<body>

    <div class="container">

        <h1 class="bg-primary" style="color:white; padding-left:15px">
            <i>i</i>-Parapheur
        </h1>
        <div class="well">
            <h2>
            ${dossierName}
                <small>
                ${nomParapheurCourant}
                </small>
            </h2>

            <p class="lead">
                Le dossier ${dossierName} a &eacute;t&eacute; supprim&eacute; par ${nomValideur}, en qualit&eacute; d'administrateur de la plate-forme.
                <br>Veuillez trouver en pi&egrave;ce jointe une fiche r&eacute;capitulative de son &eacute;tat d'avancement dans i-Parapheur au moment de la suppression.
            </p>

        </div>

        <#if footer?? && footer!="" >
        <p>
            <small>${footer}</small>
        </p>
        </#if>
    </div>

</body>
</html>
