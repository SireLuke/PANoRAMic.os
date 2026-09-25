import { ClassifiedRecord } from "./types";

export const classifiedVault: ClassifiedRecord[] = [];

export function addToClassified(record: ClassifiedRecord) {
    classifiedVault.push(record);
}

export function getClassified(category?: string) {
    if (!category) return classifiedVault;
    return classifiedVault.filter(r => r.category === category);
}
