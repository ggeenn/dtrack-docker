import deptrack

dt = deptrack.DepTrack('http://localhost:48086', 'odt_NSedF4mIzlqbexVIHpEd8tPRw1h1XAvz')
vid = dt.create_vuln('Malicious Contributor', 'Ivan Ivanov')
print(f'{vid}')
purl = 'pkg:maven/androidx.annotation/annotation@1.6.0?type=jar'
dt.assign_vuln_by_purl(purl, vid)
