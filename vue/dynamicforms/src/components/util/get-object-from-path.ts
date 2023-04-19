export default function getObjectFromPath(path: string) {
  if (path) {
    try {
      return path.split('.').reduce((res: { [key: string]: any }, val: string) => res[val] || {}, window);
    } catch (e) {
      console.error(e);
    }
  }
  return undefined;
}
