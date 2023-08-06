async function checkout(branch)
{
    var confirm_value;
    await swal({"text":`￥{LanguageCode:4009}￥`,"buttons":["￥{LanguageCode:0001}￥","￥{LanguageCode:0002}￥"]}).then((value)=>{confirm_value=value;});
    if(confirm_value)
    {
        try
        {
            const response = await axios.post("/git/checkout?branch="+branch);
            console.log(response);
            if(response.status==200)
            {
                await swal({"text":"￥{LanguageCode:4010}￥","icon":"success"});
                location.reload();
            }
        }
        catch(err)
        {
            await swal({"text":"￥{LanguageCode:4011}￥","icon":"error"});
        }
    }
}
async function new_remote_branch()
{
    var remote_branch_name;
    await swal({"text":"￥{LanguageCode:4012}￥","content":"input","buttons":["￥{LanguageCode:0001}￥","￥{LanguageCode:0002}￥"]}).then((value)=>{remote_branch_name=value;});
    if(!remote_branch_name)
    {
        return;
    }
    var remote_url;
    await swal({"text":"￥{LanguageCode:4013}￥","content":"input","buttons":["￥{LanguageCode:0001}￥","￥{LanguageCode:0002}￥"]}).then((value)=>{remote_url=value;});
    if(!remote_url)
    {
        return;
    }
    try
    {
        const response = await axios.post("/git/new_remote?name="+remote_branch_name+"&url="+remote_url);
        console.log(response)
        if(response.status==200)
        {
            await swal({"text":"新建成功。","icon":"success"});
            location.reload();
        }
    }
    catch(err)
    {
        await swal({"text":"新建失败。您可以查看服务控制台输出内容。","icon":"error"});
    }
}
async function remove_remote(name)
{
    var confirm_value;
    await swal({"text":`￥{LanguageCode:4014}￥`,"buttons":["￥{LanguageCode:0001}￥","￥{LanguageCode:0002}￥"]}).then((value)=>{confirm_value=value;});
    if(!confirm_value)
    {
        return;
    }
    try
    {
        const response = await axios.post("/git/remove_remote?name="+name);
        console.log(response)
        if(response.status==200)
        {
            await swal({"text":"￥{LanguageCode:4015}￥","icon":"success"});
            location.reload();
        }
    }
    catch(err)
    {
        await swal({"text":"￥{LanguageCode:4016}￥","icon":"error"});
    }
}
async function new_branch()
{
    var name;
    await swal({"text":"￥{LanguageCode:4017}￥","content":"input","buttons":["￥{LanguageCode:0001}￥","￥{LanguageCode:0002}￥"]}).then((value)=>{name=value;});
    if(!name)
    {
        return;
    }
    try
    {
        const response = await axios.post("/git/new_branch?name="+name);
        console.log(response)
        if(response.status==200)
        {
            await swal({"text":"新建成功。","icon":"success"});
            location.reload();
        }
    }
    catch(err)
    {
        await swal({"text":"新建失败。您可以查看服务控制台输出内容。","icon":"error"});
    }
}
async function get_status()
{
    try
    {
        const response = await axios.post("/git/status");
        console.log(response)
        if(response.status==200)
        {
            var content=decodeURIComponent(response.data.result)
            document.getElementById("status").innerHTML=content;
        }
    }
    catch(err)
    {
        await swal({"text":"￥{LanguageCode:4018}￥","icon":"error"});
    }
}
get_status();
async function stage()
{
    try
    {
        const response = await axios.post("/git/stage");
        console.log(response)
        if(response.status==200)
        {
            get_status();
            await swal({"text":"￥{LanguageCode:4019}￥","icon":"success"});
        }
    }
    catch(err)
    {
        await swal({"text":"￥{LanguageCode:4020}￥","icon":"error"});
    }
}
async function commit()
{
    var info;
    var commit_info=document.createElement("textarea");
    commit_info.setAttribute("class","form-control");
    commit_info.style.height="100px";
    commit_info.style.resize="none";
    await swal({closeOnClickOutside:false,"text":"￥{LanguageCode:4021}￥","content":commit_info,"buttons":["￥{LanguageCode:0001}￥","￥{LanguageCode:0002}￥"]}).then((value)=>{info=commit_info.value;if(!value){info="";}});
    console.log(info);
    if(!info)
    {
        return;
    }
    try
    {
        const response = await axios.post("/git/commit?info="+encodeURIComponent(info));
        console.log(response)
        if(response.status==200)
        {
            await swal({"text":"￥{LanguageCode:4022}￥","icon":"success"});
            get_status();
        }
    }
    catch(err)
    {
        await swal({"text":"￥{LanguageCode:4023}￥","icon":"error"});
    }
}
async function pull(remote,branch)
{
    var confirm_value;
    await swal({"text":`￥{LanguageCode:4024}￥`,"buttons":["￥{LanguageCode:0001}￥","￥{LanguageCode:0002}￥"]}).then((value)=>{confirm_value=value;});
    if(!confirm_value)
    {
        return;
    }
    document.getElementById("pulling-wrap").removeAttribute("hidden");
    try
    {
        const response = await axios.post(`/git/pull?remote=${remote}&branch=${branch}`);
        console.log(response)
        if(response.status==200)
        {
            await swal({"text":"￥{LanguageCode:4025}￥","icon":"success"});
            get_status();
        }
    }
    catch(err)
    {
        await swal({"text":"￥{LanguageCode:4026}￥","icon":"error"});
    }
    document.getElementById("pulling-wrap").setAttribute("hidden","true");
}
async function push(remote,branch)
{
    var confirm_value;
    await swal({"text":`￥{LanguageCode:4027}￥`,"buttons":["￥{LanguageCode:0001}￥","￥{LanguageCode:0002}￥"]}).then((value)=>{confirm_value=value;});
    if(!confirm_value)
    {
        return;
    }
    document.getElementById("pushing-wrap").removeAttribute("hidden");
    try
    {
        const response = await axios.post(`/git/push?remote=${remote}&branch=${branch}`);
        console.log(response)
        if(response.status==200)
        {
            await swal({"text":"￥{LanguageCode:4028}￥","icon":"success"});
            get_status();
        }
    }
    catch(err)
    {
        await swal({"text":"￥{LanguageCode:4029}￥","icon":"error"});
    }
    document.getElementById("pushing-wrap").setAttribute("hidden","true");
}