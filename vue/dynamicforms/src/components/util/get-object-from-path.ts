export default function getObjectFromPath(path: string) {
  if (path) {
    return path.split('.').reduce((res: { [key: string]: any }, val: string) => res[val] ?? {}, window);
  }
  return undefined;
}
