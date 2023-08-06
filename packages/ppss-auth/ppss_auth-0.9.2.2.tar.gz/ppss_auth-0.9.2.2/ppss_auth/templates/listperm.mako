<%inherit file="${context['midtpl']}" />

<table class="table">
	<thead>
		<tr>
			<th>${_('Name')}</th>
			<th>${_('System')}</th>
		</tr>
	</thead>
	<tbody>
		%for i,e in enumerate(elements):
			<tr>
				<td>${e.name}</td>
				<td>${_("Yes") if e.permtype == 1 else _("No")}</td>
				<td>
					<a class="btn btn-success" href="${request.route_url('ppss:perm:edit',elementid=e.id)}">${_('delete')}</a><br/>
					<!--a href="${request.route_url('ppss:user:changepassword',userid=e.id)}">modify</a><br/-->

				 </td>
			</tr>
		%endfor

	</tbody>


</table>

<div>
	<a class="btn btn-success" href="${request.route_url('ppss:perm:edit',elementid = -1)}">${_('Add Perm')}</a>
</div>