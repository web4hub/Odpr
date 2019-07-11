export default function getByKey (object, key) {
	key = key.replace(/\[(\w+)\]/g, '.$1') // convert indexes to properties
	key = key.replace(/^\./, '') // strip a leading dot
	let a = key.split(/[/.]/)
	for (let i = 0, n = a.length; i < n; ++i) {
		let k = a[i]
		if (k in object) {
			object = object[k]
		} else {
			return
		}
	}
	return object
}
