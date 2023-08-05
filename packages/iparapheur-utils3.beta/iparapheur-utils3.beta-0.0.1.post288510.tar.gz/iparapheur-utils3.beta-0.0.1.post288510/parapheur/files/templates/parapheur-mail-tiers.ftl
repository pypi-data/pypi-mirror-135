Votre dossier '${dossierName}'
<#if reason == "reject">
 vient d'être rejeté.
<#else>

<#if actionEffectuee == "TDT">
 a été; télétransmis avec succès par ${nomValideur}, et est prêt à être récupéré ou archivé.

<#else>
 vient d'être visé/signé par ${nomValideur}
    <#if actionDemandee == "ARCHIVAGE">, et est prêt pour être récupéré, télétransmis ou archivé
    </#if>
.
</#if>
</#if>
