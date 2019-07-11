export default function getByKey (object, array) {
	for (let i = 0, n = array.length; i < n; ++i) {
		let k = array[i]
		if (k in object) {
			object = object[k]
		} else {
			return
		}
	}
	return object
}
