export default function getObjectFromPath(path: string) {
  if (path) {
    try {
      // @ts-ignore
      return path.split('.').reduce((res, val) => res[val] || {}, window)
    } catch (e) {
      console.error(e);
    }
  }
  return undefined;
}
