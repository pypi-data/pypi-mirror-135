function GetQueryString(name)
{
    var reg=new RegExp("(^|&)" + name + "=([^&]*)(&|$)");
    var r=window.location.search.substr(1).match(reg);
    if (r!=null)
    {
        return unescape(r[2]);
    }
    return null;
}
function compare_version(v1,v2)
{
    var va=v1.split("."),vb=v2.split(".");
    if(parseInt(va[0])<parseInt(vb[0]))
    {
        return "<";
    }
    if(parseInt(va[0])>parseInt(vb[0]))
    {
        return ">";
    }
    if(parseInt(va[1])<parseInt(vb[1]))
    {
        return "<";
    }
    if(parseInt(va[1])>parseInt(vb[1]))
    {
        return ">";
    }
    if(parseInt(va[2])<parseInt(vb[2]))
    {
        return "<";
    }
    if(parseInt(va[2])>parseInt(vb[2]))
    {
        return ">";
    }
    return "=";
}