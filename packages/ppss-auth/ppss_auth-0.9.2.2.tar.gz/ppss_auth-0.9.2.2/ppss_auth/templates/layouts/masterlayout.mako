<html>
<head>
  <title>Login page</title>
  <meta charset="UTF-8">
	<meta name="viewport" content="width=device-width, initial-scale=1.0">
  <%block name="bootstrapcss">
    <%include file="../shared/bootstrapcss.html"/>
  </%block>
  <%block name="ppssauth_css">
     <link rel="stylesheet" href="${ request.static_url('ppss_auth:ppss_auth_static/ppssauth.css') }"/>
  </%block>

  <%block name="ppssauth_headerjs">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/handlebars.js/4.1.0/handlebars.min.js"></script>
    <script
          src="https://code.jquery.com/ui/1.12.1/jquery-ui.min.js"
          integrity="sha256-VazP97ZCwtekAsvgPBSUwPFKdrwD3unUfSGVYrahUqU="
          crossorigin="anonymous"
    ></script>
  </%block>

</head>
<body class="ppss_auth">
${next.body()}


<%block name="ppssauth_footerjs">
<script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js" integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossorigin="anonymous"></script>
</%block>

</body>

</html>
