<%inherit file="${context['midtpl']}" />
<% passwordexpire = request.ppssauthconf.passwordexpire %>
<table class="table">
	<thead>
		<tr>
			<th>${_('Username')}</th>
			<th>${_('Enabled')}</th>
			%if passwordexpire:
				<th>${_('Password expires')}</th>
			%endif
			<th>${_('Last access')}</th>
			<th>${_('Action')}</th>
		</tr>
	</thead>
	<tbody>
		%for i,e in enumerate(elements):
			<tr>
				<td>${e.username}</td>
				<td>${_("Yes") if e.enabled else _("No")}</td>
				%if passwordexpire:
					<th>${e.passwordexpire.strftime( _('%m/%d/%Y') ) if e.passwordexpire else " - "}</th>
				%endif
				<td>${e.lastlogin.strftime('%Y-%m-%d') if e.lastlogin else " - "}</td>
				<td>
					<a class="btn btn-success" href="${request.route_url('ppss:user:edit',elementid=e.id)}">${_('modify')}</a><br/>

				 </td>
			</tr>
		%endfor

	</tbody>


</table>

<div>
	<a class="btn btn-success" href="${request.route_url('ppss:user:edit',elementid = -1)}">${_('Add User')}</a>
</div>