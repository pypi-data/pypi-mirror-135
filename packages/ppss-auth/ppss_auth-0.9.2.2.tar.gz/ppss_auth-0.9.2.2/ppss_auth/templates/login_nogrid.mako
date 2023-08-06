<%inherit file="${context['logintpl']}" />
<form action="${request.route_url('ppsslogin')}" method="POST" class="loginform">
    <input type="hidden" value="${get_csrf_token()}" name="csrf_token">
    <input class="form-control" type="text" name="${_('username')}" placeholder="username">
    <br/>
    <input class="form-control" type="password" name="${_('password')}" placeholder="password">
    <br/>
    <div class="text-center">
        <input class="btn btn-success" type="submit" name="submit" value="${_('Login')}"/>
    </div>
    </br>
    <p class="text-danger">${msg}</p>
</form>