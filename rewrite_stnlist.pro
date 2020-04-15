pro rewrite_stnlist

spawn,'touch ../PHA2015/pha52jgo/data/hadisdh/7319q/meta/7319q_metadata_file.txt'
spawn,'touch ../PHA2015/pha52jgo/data/hadisdh/7319e/meta/7319e_metadata_file.txt'
spawn,'touch ../PHA2015/pha52jgo/data/hadisdh/7319rh/meta/7319rh_metadata_file.txt'
spawn,'touch ../PHA2015/pha52jgo/data/hadisdh/7319t/meta/7319t_metadata_file.txt'
spawn,'touch ../PHA2015/pha52jgo/data/hadisdh/7319td/meta/7319td_metadata_file.txt'
spawn,'touch ../PHA2015/pha52jgo/data/hadisdh/7319tw/meta/7319tw_metadata_file.txt'
spawn,'touch ../PHA2015/pha52jgo/data/hadisdh/7319dpd/meta/7319dpd_metadata_file.txt'
spawn,'touch ../PHA2015/pha52jgo/data/hadisdh/7319slp/meta/7319slp_metadata_file.txt'
spawn,'touch ../PHA2015/pha52jgo/data/hadisdh/7319ws/meta/7319ws_metadata_file.txt'

stop
openr,5,'../../LISTS_DOCS/goodforHadISDH.4.2.0.2019f_JAN2020.txt'
openw,10,'../PHA2015/pha52jgo/data/hadisdh/7319q/meta/7319q_stnlist.tavg'
openw,11,'../PHA2015/pha52jgo/data/hadisdh/7319e/meta/7319e_stnlist.tavg'
openw,12,'../PHA2015/pha52jgo/data/hadisdh/7319rh/meta/7319rh_stnlist.tavg'
openw,13,'../PHA2015/pha52jgo/data/hadisdh/7319t/meta/7319t_stnlist.tavg'
openw,14,'../PHA2015/pha52jgo/data/hadisdh/7319td/meta/7319td_stnlist.tavg'
openw,15,'../PHA2015/pha52jgo/data/hadisdh/7319tw/meta/7319tw_stnlist.tavg'
openw,16,'../PHA2015/pha52jgo/data/hadisdh/7319dpd/meta/7319dpd_stnlist.tavg'
openw,17,'../PHA2015/pha52jgo/data/hadisdh/7319slp/meta/7319slp_stnlist.tavg'
openw,18,'../PHA2015/pha52jgo/data/hadisdh/7319ws/meta/7319ws_stnlist.tavg'
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
