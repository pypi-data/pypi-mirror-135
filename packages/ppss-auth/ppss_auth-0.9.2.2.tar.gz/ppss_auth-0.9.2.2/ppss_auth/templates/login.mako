<%inherit file="${context['logintpl']}" />
<div class="container">
    <div class="row text-center">
        <div class="${bc['xs']}12 col-md-4 offset-md-4">
            <form class="my-5" action="${request.route_url('ppsslogin')}" method="POST" class="loginform">
                <input type="hidden" value="${get_csrf_token()}" name="csrf_token">
                <h1 class="h3 mb-3 font-weight-normal">${_("Please sign in")}</h1>
                % if request.loggeduser: 
                <p>
                    ${_('You are already logged in as')} <a href="${request.route_url('ppss:user:editself')}">${request.loggeduser.username}</a>.<br/> 
                    ${signinreason}
                </p>
                % endif
                <input class="form-control" type="text" name="username" placeholder="${_('username')}" class="form-control">
                <br/>
                <input class="form-control" type="password" name="password" placeholder="${_('password')}" class="form-control">
                <br/>
                <div class="text-center">
                    <input class="btn btn-success" type="submit" name="submit" value="${_('Login')}"/>
                    % if ppsauthconf.usercanregister:
                    <br>
                    <small>${_('Not registered yet?')} <a href="${request.route_url('ppss:user:register')}">${_('Register now')}</a></small>
                    % endif
                </div>
                </br>
                <p class="text-danger">${msg}</p>
            </form>
        </div>
    </div>
</div>