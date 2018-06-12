UNIQ = ".|unique"
INITIALIZE = '. as $data | $data.{path} = (if $data.{path} then $data.{path} else {value} end)'
TAG_OCDS = '. as $data | $data.tags |= ["{default}"]|.tags += (if $data.contracts then ["contract"] else [] end)|.tags += (if $data.awards then ["award"] else [] end)'
TAG_ROLES = '.{path} | if type=="array" then map(.roles+=["{role}"]) else .roles+=["{role}"] end'
