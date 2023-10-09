import { IView } from './namespace';
import ViewGeneric from './view-generic';

export default class ViewApi<T> extends ViewGeneric<T> implements IView<T> {
  constructor(url: string) {
    const baseUrl = url.replace(/\/+$/, '');
    const trailingSlash = `${baseUrl}/`;
    super(baseUrl, trailingSlash, trailingSlash, trailingSlash);
  }
}
