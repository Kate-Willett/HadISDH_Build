pro rewrite_stnlist

openr,5,'goodforHadCRUH_FEB2013.txt'
openw,7,'hadisdh7312_stnlist.tavg'
while not eof(5) do begin
  inid=''
  inlat=0.
  inlon=0.
  inelev=0.
  incid=''
  innamoo=''
  mush='' 
  readf,5,inid,inlat,inlon,inelev,incid,innamoo,format='(a11,f8.4,f10.4,f7.1,x,a2,x,a29,13x)'
  printf,7,inid,inlat,inlon,inelev,incid,innamoo,format='(a11,f7.2,f10.2,8x,i5,x,a2,x,a29)'
endwhile
close,5
close,7

end
