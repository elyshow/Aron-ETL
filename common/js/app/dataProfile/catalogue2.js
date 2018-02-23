$(function(){
	$("#mylist2").datagrid({
		url: "/huafeng/catalogue2_table/",
		method:'post',
		toolbar:'#toolbar',
		onClickRow:function(row){
			domDetail()
		},
		onDblClickRow:function(row){
			domDetail()
		},
		columns:[[
			{field:'cataloguename',title:'目录或资源名称',width:'59%',align:'left'},
			{field:'typetime',title:'建立时间',width:'30%',align:'left'},
			{field:'count',title:'资源数量',width:'10%',align:'center'},
			{field:'typeid',title:'目录id',width:'0%',align:'center',hidden:'true'},
        ]],
	})
	$('#search').searchbox({
        prompt:'请输入目录或资源名称',
        height:24,
        width:200,
        searcher:function(v,n){
           $('#mylist2').datagrid('load', {condition:v})
        }
    })
})

function domDetail() {
	var data = $("#mylist2").datagrid('getSelected');
	data_typeid=data.typeid;
	console.log(data);
	console.log(data_typeid);
	$.get('/huafeng/table_request/',{data:data_typeid},function(msg){
		window.open('/huafeng/table/','_self')
		$("#mylist2").datagrid('unselectAll')
	})
}