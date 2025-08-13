import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";

const SingleSelectBox = (): React.ReactElement => {
  // 검색 완료로 만들자.
  return (
    <Select>
      <SelectTrigger className="w-2/3`">
        <SelectValue placeholder="Theme" />
      </SelectTrigger>
      <SelectContent position="popper">
        <SelectItem value="light">Light</SelectItem>
        <SelectItem value="dark">Dark</SelectItem>
        <SelectItem value="system">System</SelectItem>
      </SelectContent>
    </Select>
  );
};

export { SingleSelectBox };
