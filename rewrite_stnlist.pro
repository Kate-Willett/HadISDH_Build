pro rewrite_stnlist

spawn,'touch ''../PHA2015/pha52jgo/data/hadisdh/7318q/meta/7318q_metadata_file.txt'
spawn,'touch ''../PHA2015/pha52jgo/data/hadisdh/7318e/meta/7318e_metadata_file.txt'
spawn,'touch ''../PHA2015/pha52jgo/data/hadisdh/7318rh/meta/7318rh_metadata_file.txt'
spawn,'touch ''../PHA2015/pha52jgo/data/hadisdh/7318t/meta/7318t_metadata_file.txt'
spawn,'touch ''../PHA2015/pha52jgo/data/hadisdh/7318td/meta/7318td_metadata_file.txt'
spawn,'touch ''../PHA2015/pha52jgo/data/hadisdh/7318tw/meta/7318tw_metadata_file.txt'
spawn,'touch ''../PHA2015/pha52jgo/data/hadisdh/7318dpd/meta/7318dpd_metadata_file.txt'
spawn,'touch ''../PHA2015/pha52jgo/data/hadisdh/7318slp/meta/7318slp_metadata_file.txt'
spawn,'touch ''../PHA2015/pha52jgo/data/hadisdh/7318ws/meta/7318ws_metadata_file.txt'


openr,5,'../../LISTS_DOCS/goodforHadISDH.4.1.0.2018f_JAN2019.txt'
openw,10,'../PHA2015/pha52jgo/data/hadisdh/7318q/meta/7318q_stnlist.tavg'
openw,11,'../PHA2015/pha52jgo/data/hadisdh/7318e/meta/7318e_stnlist.tavg'
openw,12,'../PHA2015/pha52jgo/data/hadisdh/7318rh/meta/7318rh_stnlist.tavg'
openw,13,'../PHA2015/pha52jgo/data/hadisdh/7318t/meta/7318t_stnlist.tavg'
openw,14,'../PHA2015/pha52jgo/data/hadisdh/7318td/meta/7318td_stnlist.tavg'
openw,15,'../PHA2015/pha52jgo/data/hadisdh/7318tw/meta/7318tw_stnlist.tavg'
openw,16,'../PHA2015/pha52jgo/data/hadisdh/7318dpd/meta/7318dpd_stnlist.tavg'
openw,17,'../PHA2015/pha52jgo/data/hadisdh/7318slp/meta/7318slp_stnlist.tavg'
openw,18,'../PHA2015/pha52jgo/data/hadisdh/7318ws/meta/7318ws_stnlist.tavg'
while not eof(5) do begin
  inid=''
  inlat=0.
  inlon=0.
  inelev=0.
  incid=''
  innamoo=''
  mush='' 
  readf,5,inid,inlat,inlon,inelev,incid,innamoo,format='(a11,f8.4,f10.4,f7.1,x,a2,x,a29,13x)'
  printf,10,inid,inlat,inlon,inelev,incid,innamoo,format='(a11,f7.2,f10.2,8x,i5,x,a2,x,a29)'
  printf,11,inid,inlat,inlon,inelev,incid,innamoo,format='(a11,f7.2,f10.2,8x,i5,x,a2,x,a29)'
  printf,12,inid,inlat,inlon,inelev,incid,innamoo,format='(a11,f7.2,f10.2,8x,i5,x,a2,x,a29)'
  printf,13,inid,inlat,inlon,inelev,incid,innamoo,format='(a11,f7.2,f10.2,8x,i5,x,a2,x,a29)'
  printf,14,inid,inlat,inlon,inelev,incid,innamoo,format='(a11,f7.2,f10.2,8x,i5,x,a2,x,a29)'
  printf,15,inid,inlat,inlon,inelev,incid,innamoo,format='(a11,f7.2,f10.2,8x,i5,x,a2,x,a29)'
  printf,16,inid,inlat,inlon,inelev,incid,innamoo,format='(a11,f7.2,f10.2,8x,i5,x,a2,x,a29)'
  printf,17,inid,inlat,inlon,inelev,incid,innamoo,format='(a11,f7.2,f10.2,8x,i5,x,a2,x,a29)'
  printf,18,inid,inlat,inlon,inelev,incid,innamoo,format='(a11,f7.2,f10.2,8x,i5,x,a2,x,a29)'
endwhile
close,5
close,/all


end
